from flask import g, current_app
from opensearchpy import OpenSearch

# Create an OpenSearch client instance and put it into Flask shared space for use by the application
def get_opensearch():
    if 'opensearch' not in g:
        #### Step 4.a:
        # Implement a client connection to OpenSearch so that the rest of the application can communicate with OpenSearch
        g.opensearch = OpenSearch(
            hosts=[{'host': 'localhost', 'port': 9200}],
            http_compress=True,  # enables gzip compression for request bodies
            http_auth=('admin', 'admin'),
            use_ssl=True,
            verify_certs=False,
            ssl_assert_hostname=False,
            ssl_show_warn=False,
        )

    return g.opensearch

def create_index(index_name, index_body):
    client = get_opensearch()
    
    if client.indices.exists(index_name):
        client.indices.delete(index_name)
    
    return client.indices.create(index_name, index_body)