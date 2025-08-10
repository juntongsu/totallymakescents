import streamlit as st 

path_total = 'https://raw.githubusercontent.com/juntongsu/totallymakescents/refs/heads/main/'
img_path = path_total+'app/images/'

st.title('Meet the Team')

img1, txt1 = st.columns([1, 2])
img1.image(img_path+'elly.png')
txt1.subheader('Ngan (Elly) Do')
txt1.markdown("[![Repo](https://badgen.net/badge/github/Github/purple?icon&label)](https://github.com/ellydo17)", unsafe_allow_html=True)
txt1.write('I like to travel!')
# with search1:
#     with st.expander("Elly's Favorite Search"):
#         st.link_button('A magical scent :crystal_ball: in a mystical forest :evergreen_tree: with herbs :herb: and secrets:no_mouth:.', '')

img2, txt2 = st.columns([1, 2])
img2.image(img_path+'fernando.jpg')
txt2.subheader('Fernando Liu Lopez')
txt2.markdown("[![Repo](https://badgen.net/badge/github/Github/green?icon&label)](https://github.com/fernando-liu-lopez)", unsafe_allow_html=True)
txt2.write(' ')
# with search2:
#     with st.expander("Fernando's Favorite Search"):
#         st.link_button('A floral scent :blossom: with hints of jasmine :bouquet:.', '')
#         st.link_button('A woody fragrance :deciduous_tree: with notes of cedar :evergreen_tree:.', '')
#         st.link_button('A citrusy aroma :lemon: with a touch of bergamot :tangerine:.', '')

img4, txt4 = st.columns([1, 2])
img4.image(img_path+'su.jpg')
txt4.subheader('Juntong Su')
txt4.markdown("[![Repo](https://badgen.net/badge/github/Github/pink?icon&label)](https://github.com/juntongsu)", unsafe_allow_html=True) 
txt4.markdown("[![Repo](https://badgen.net/badge/personal/website/pink)](https://juntongsu.github.io)", unsafe_allow_html=True)
txt4.write('Panda, an animal, eats shoots and leaves.')
# with search4:
#     with st.expander("Su's Favorite Search"):
#         st.link_button('A bittersweet scent :performing_arts: for a farewell party :balloon:.', '')

st.divider()
st.markdown(":red-badge[❤️ Special Thanks To ❤️]")
st.markdown('#### Yevgeniya (Jonah) Tarasova')
st.markdown("[![Repo](https://badgen.net/badge/github/Github/red?icon&label)](https://github.com/jtarasov)", unsafe_allow_html=True)
st.markdown('#### Katherine Martin')
st.markdown("[![Repo](https://badgen.net/badge/github/Github/blue?icon&label)](https://github.com/kmerkl22)", unsafe_allow_html=True)

# img5, txt5, img3, txt3, search3, search5 = st.columns(6)
# img5.image(img_path+'su.png')
# txt5.markdown('#### Jonah')
# txt5.markdown("[![Repo](https://badgen.net/badge/github/Github/red?icon&label)](https://github.com/jtarasov)", unsafe_allow_html=True)
# txt5.write(' ')

# img3.image(img_path+'katherine.jpg')
# txt3.markdown('#### Katherine')
# txt3.markdown("[![Repo](https://badgen.net/badge/github/Github/blue?icon&label)](https://github.com/kmerkl22)", unsafe_allow_html=True)
# search3.write('I enjoy reading and painting.')
# with search3:
#     with st.expander("Katherine's Favorite Search"):
#         st.link_button('Fruity perfume :pineapple: that is vibrant, fresh, and full of energy :sparkler:.', '')