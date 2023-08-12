TODOS:

pinecone vector database:
setup: vectorize therapy categories (openai embeddings) and insert into pinecone
flow:
1. when user asks a question, search pinecone for top 15 similar categories
2. tell chat gpt to pick the top 3 categories out of the 15
3. have chat gpt research and generate summary of the 3 category websites specific for user question

website summarization flow:
1. scrape html
2. clean html
3. tell chat gpt to summarize with respect to (user question / chat history)