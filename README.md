# TotallyMakeScents
##### Juntong Su, Ngan (Elly) Do, and Fernando Liu Lopez

## Introduction

### Workflow
```mermaid
    ---
    config:
    theme: redux
    layout: dagre
    ---
    flowchart TB
        A["Users Data"] --> B(["Collaborative Filtering"])
        B --> C["List from Users"]
        n1["Notes Data"] --> n3(["Content Based Filtering"])
        n3 --> n4["List from Notes"]
        C --> n5["Combined List"]
        n4 --> n5
        n5 --> n6["Reordered List"]
        n2["Full Data"] --> n7["Summary of Reviews"]
        u1["User Query"] --> n8["Ranked Subthemes"]
        n8 --> n9["Generated Tags"]
        n7 --> n10(["SentenceBERT"])
        n9 --> n10
        n10 --> n11["List of Perfumes"]
        n11 --> n12["Reordered List"] & n18["Testing"] & n20["Visualization"]
        n12 --> n13["Generated Text Explanations"]
        n14["Kaggle"] --> n1 & n22["Reviews Data"]
        n15["Fragrantica"] -- FKS --> n2
        n16["Published Paper"] --> A
        n5 --> n17["Testing"] & n19["Visualization"]
        n21["Key Characteristics"] --> n20 & n10
        n2 --> n21
        n22 --> n2
        n6 --> n23["TotallyMakeScents DS"]
        n19 --> n23
        n13 --> n24["TotallyMakeScents DL"]
        n20 --> n24
        A@{ shape: db}
        C@{ shape: lin-proc}
        n1@{ shape: db}
        n4@{ shape: lin-proc}
        n5@{ shape: lin-proc}
        n6@{ shape: lin-proc}
        n2@{ shape: disk}
        n7@{ shape: disk}
        u1@{ shape: doc}
        n8@{ shape: docs}
        n9@{ shape: tag-doc}
        n11@{ shape: lin-proc}
        n12@{ shape: lin-proc}
        n18@{ shape: paper-tape}
        n20@{ shape: paper-tape}
        n13@{ shape: procs}
        n14@{ shape: das}
        n22@{ shape: cyl}
        n15@{ shape: das}
        n16@{ shape: das}
        n17@{ shape: paper-tape}
        n19@{ shape: paper-tape}
        n21@{ shape: disk}
```

### Repository Structure
```text
totallymakescents/
├── app/
│   ├── pages/
│   │   ├── home.py
│   │   └── tms1.py
│   └── images/
│   ├── totallymakescents.py
├── data/
│   ├── combined_df_classify_reviews.parquet
├── web_scraping/
├── data_analysis/
├── generated_data/
├── models/
├── recommender/
├── tests/
└── README.md        

Note: The full tree will be generated once we have cleaned up the repo

## Data
Our primary datasets were the publicly available (1) [Fragrantica dataset](https://www.kaggle.com/datasets/olgagmiufana1/fragrantica-com-fragrance-dataset) from Kaggle, which contains basic information about perfumes, including their notes and accords, and another (2) [Fragrantica dataset](https://www.kaggle.com/datasets/joehusseinmama/fragrantica-data/data) that shares many perfumes with the first one but also includes a “reviews” column. To enhance our data, we developed custom (3) [web-scraping functions](https://github.com/juntongsu/totallymakescents/blob/main/web_scraping/frag_perf_scrape.ipynb) capable of doubling both the size of the database and the number of available features (see Figure 1). Due to time constraints, the full compilation of the improved dataset was consigned as a future objective. However, we repurposed the scraping tools to operate in the background at runtime once recommendations are generated, ensuring users to see detailed information about their recommended perfumes (see Figure 2).

<figure>
  <img src="https://docs.google.com/document/d/1WRvKoKcWSfjRiFXRX5AFMJU_BE2a6tHlMiJMigyyJio/edit?usp=sharing" alt="Figure 1" width=80%>
  <figcaption>Figure 1.</figcaption>
</figure>

<figure>
  <img src="https://docs.google.com/document/d/1WRvKoKcWSfjRiFXRX5AFMJU_BE2a6tHlMiJMigyyJio/edit?tab=t.8u35tbo61hib" alt="Figure 2">
  <figcaption>Figure 2.</figcaption>
</figure>

For model training, we combined (4) [scraped data](https://github.com/juntongsu/totallymakescents/blob/main/web_scraping/frag_notes_scrape.ipynb) from Fragrantica and FindaScent, synthetically generated perfume descriptions (5) [1](https://github.com/juntongsu/totallymakescents/blob/main/generated_data/perfume_descriptions.csv) (6) [2](https://github.com/juntongsu/totallymakescents/blob/main/generated_data/perfume_descriptions_creative.csv), and hand-crafted data. The (7) [descriptive perfume data](https://github.com/juntongsu/totallymakescents/blob/main/generated_data/findascent_note_descriptions.csv) and perfume descriptions were used to allow models to understand perfume notes and the sensory language associated with each. Additionally, we developed (8) [scripts](https://github.com/juntongsu/totallymakescents/blob/main/generated_data/generating_training_data.ipynb) to generate a (9) [question-answer training set](https://github.com/juntongsu/totallymakescents/blob/main/generated_data/training_data_chatml.jsonl) designed to generate relevant perfume notes from abstract queries and situational prompts.


## Model
Our recommender combines two models: mistral-7B-v0.3 and all-MiniLM-L6-v2. We applied continued pre-training to Mistral using 2055 entries of descriptive perfume data, using it to generate natural-language explanations connecting recommendations to the user’s query. In addition, we experimented with a fine-tuned Unsloth/LLaMA-3.2-3B-Instruct model to generate similarly styled explanations with smaller memory and compute requirements. We further fine-tuned Mistral with 2000 question-answer pairs mapping abstract perfume queries to relevant perfume notes. The user’s query and the generated tags were then passed to the semantic search model all-MiniLM-L6-v2. The tags expanded the vocabulary through which the model could produce associations, allowing for more relevant recommendations. Furthermore, the tags accounted for users whose queries were brief, abstract, or lacking in specialized perfume terminology.

After obtaining the embeddings for the user's query and the generated tags, we proceed to compare them to the perfume embeddings generated from our primary datasets. To build the perfume embeddings, we combined notes, accords, and user reviews, where reviews were first classified by sentiment using a (10) [pretrained DistilBERT model](https://huggingface.co/distilbert/distilbert-base-uncased-finetuned-sst-2-english), with positive reviews receiving higher weights. Based on embedding similarity, we return the top-k most relevant perfumes to user query.


## Testing
We tested our system on two query types: standard and non-standard, based on different levels of user experience. Experienced users, who are familiar with perfume terms, might ask standard queries such as “I want something {accord} with {note1} and {note2} for {occasion}”. These queries contain direct references to perfume-related terms, so we skip the tag generation step and feed them directly into the BERT-model for scoring. On the other hand, non-standard queries such as “What perfumes capture the essence of a natural new home?” potentially from new users who do not know perfume-related vocabulary. For these, we use an LLM to generate accord-related and note-related tags before performing the recommendations. 

Each model returns the top-3 perfumes per query. Without ground truth, we used human preference labeling: Yes (1) means the perfume is well-related to the query, and no (0) means the perfume is poorly related.

We then averaged the “yes” ratios across all ratings. The final results tell us that our models perform consistently well on both types of queries :
Without tags (standard queries): Average fraction of relevant items in top-k = 0.89, or 89% (across 34 queries and 102 ratings).
With tags (non-standard queries): Average fraction of relevant items in top-k = 0.88, or 88% (across 34 queries and 102 ratings).

## Future

## Acknowledgements
