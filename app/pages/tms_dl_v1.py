import streamlit as st
from st_files_connection import FilesConnection
from pathlib import Path
import gdown
import torch
from unsloth import FastLanguageModel
from unsloth.chat_templates import get_chat_template
from sentence_transformers import SentenceTransformer, util
import pandas as pd
from transformers import TextStreamer
# from transformers import AutoTokenizer, AutoModel

conn = st.connection('gcs', type=FilesConnection)

st.title("Perfume Recommendation with Explanation")
st.write("🌀 Starting app...")

@st.cache_resource
def download_model(model_folder_name, folder_id):
    save_dest = Path('model')
    save_dest.mkdir(exist_ok=True)
    
    local_model_path = Path(f"model/{model_folder_name}")

    if not local_model_path.exists():
        local_model_path.mkdir(exist_ok=True)
    if not any(local_model_path.iterdir()):
        with st.spinner("Downloading model... this may take awhile! \n Don't stop it!"):
            folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
            gdown.download_folder(folder_url, output=str(local_model_path), quiet=True, use_cookies=False)
    return local_model_path

@st.cache_resource
def load_model():
    llama_model_path = download_model('llama-model', '1prAmxGlje5ruqlrVCp7UB5zt3OGltmX1')
    model, tokenizer = FastLanguageModel.from_pretrained(
        model_name=str(llama_model_path),
        max_seq_length=2048,
        dtype=None,
        load_in_4bit=True,
    )
    tokenizer = get_chat_template(tokenizer, chat_template="llama-3.1")
    FastLanguageModel.for_inference(model)
    return model, tokenizer

@st.cache_resource
def load_sbert():
    return SentenceTransformer("all-MiniLM-L6-v2")

@st.cache_resource
def load_embeddings():
    with conn.open(f"gs://totallymakescents/perfume_embeddings.pt", "rb") as f:
        embeddings = torch.load(f)
    return embeddings

@st.cache_resource
def load_dataframe():
    return conn.read('gs://totallymakescents/data/combined_df_classify_reviews.parquet', input_format="parquet", ttl=600)


try:
    st.write("🔧 Loading model...")
    model, tokenizer = load_model()
    st.success("✅ Model loaded!")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")
    st.stop()

try:
    st.write("📔 Loading SBERT...")
    sbert_model = load_sbert()
    st.success("✅ SBERT loaded!")
except Exception as e:
    st.error(f"❌ Error loading SBERT: {e}")
    st.stop()

try:
    st.write("💐 Loading perfume embeddings...")
    perfume_embeddings = load_embeddings()
    st.success("✅ Embeddings loaded!")
except Exception as e:
    st.error(f"❌ Error loading embeddings: {e}")
    st.stop()

try:
    st.write("📄 Loading data...")
    combined_df_classify_reviews = load_dataframe()
    st.success("✅ Data loaded!")
except Exception as e:
    st.error(f"❌ Error loading data: {e}")
    st.stop()

#input format for LLM
def format_for_explanation(user_query, perfume_row):
    short_desc = (
        f"Top Notes: {perfume_row['Top']}. "
        f"Middle Notes: {perfume_row['Middle']}. "
        f"Base Notes: {perfume_row['Base']}. "
        f"Main Accords: {', '.join([str(perfume_row.get(f'mainaccord{i}', '')) for i in range(1, 6)])}."
    )
    return {
        "role": "user",
        "content": (
            f"User query: {user_query}\n"
            f"Perfume returned: {perfume_row['Perfume']} by {perfume_row['Brand']}\n"
            f"Notes: {short_desc}\n"
            f"Please explain why this perfume fits the request."
        )
    }


user_query = st.text_input("Describe your scent preference:", placeholder="e.g. Looking for a bittersweet scent for a farewell party.")
top_k = st.slider("Number of Recommendations", min_value=1, max_value=5, value=3)

if st.button("Recommend and Explain") and user_query:
    with st.spinner("Finding matches and generating explanations..."):

      query_embedding = sbert_model.encode(user_query, convert_to_tensor=True)
      scent_tensor = perfume_embeddings.to(query_embedding.device)

      similarities = util.cos_sim(query_embedding, scent_tensor)[0]
      top_results = torch.topk(similarities, k=top_k)

      for score, idx in zip(top_results.values, top_results.indices):
          idx = idx.item()
          perfume = combined_df_classify_reviews.iloc[idx]
          message = format_for_explanation(user_query, perfume)

          inputs = tokenizer.apply_chat_template(
              [message],
              tokenize=True,
              add_generation_prompt=True,
              return_tensors="pt",
          ).to("cuda")

          text_streamer = TextStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True)
          with st.expander(f"{perfume['Perfume']} by {perfume['Brand']} (Score: {score.item():.3f})", expanded=True):
              short_desc = (
                  f"Top Notes: {perfume['Top']}. "
                  f"Middle Notes: {perfume['Middle']}. "
                  f"Base Notes: {perfume['Base']}. "
                  f"Main Accords: {', '.join([str(perfume.get(f'mainaccord{i}', '')) for i in range(1, 6)])}."
              )

              st.markdown(f"**Notes**: {short_desc}")

              output_llm = model.generate(
                    input_ids=inputs,
                    max_new_tokens=256,
                    use_cache=True,
                    temperature=1.5,
                    min_p=0.1,
                )

              full_output_llm = tokenizer.decode(output_llm[0], skip_special_tokens=True)

              assistant_prefix = "assistant\n"
              if assistant_prefix in full_output_llm:
                  llm_explanation = full_output_llm.split(assistant_prefix, 1)[-1].strip()
              else:
                  llm_explanation = full_output_llm.replace(message["content"], "").strip()

              st.markdown("**Explanation:**")
              st.markdown(llm_explanation)