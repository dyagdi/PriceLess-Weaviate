import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.config import Configure, Property, DataType, Configure, VectorDistances
from datamodels import ProductObject
from client_connector import get_client


def adjust_first_letter_of_collection_name(collection_name):
    return collection_name[0].upper() + collection_name[1:]




from weaviate.classes.config import DataType, Property

def build_properties_from_product_objects():
    datamodel_properties = ProductObject.get_property_names(ProductObject)
    schema_properties = []

    for prop in datamodel_properties:
        if prop == "id":
            continue
        elif prop == "in_stock":
            schema_properties.append(Property(name=prop, data_type=DataType.BOOL))
        elif prop in ["price", "high_price"]:
            schema_properties.append(Property(name=prop, data_type=DataType.NUMBER))
        else:
            schema_properties.append(Property(name=prop, data_type=DataType.TEXT))

    return schema_properties

def create_new_collection(collection_name):

    client = get_client()
    
    schema_properties = build_properties_from_product_objects()

    new_collection = client.collections.create(
        name=collection_name,
        vectorizer_config=Configure.Vectorizer.text2vec_openai(model="text-embedding-3-large"),
        generative_config=Configure.Generative.openai(),
        properties=schema_properties,
        # reranker_config=Configure.Reranker.cohere(
        #     model="rerank-multilingual-v3.0"  # Use multilingual model since your content is in Turkish
        # ),
        vector_index_config=Configure.VectorIndex.hnsw(  # Other available options: `flat` or `dynamic`
            distance_metric=VectorDistances.COSINE,
            # quantizer=Configure.VectorIndex.Quantizer.bq(),
        )
    )

    collection_name = adjust_first_letter_of_collection_name(collection_name)

    status = True if new_collection.name == collection_name else False

    client.close()

    return status

