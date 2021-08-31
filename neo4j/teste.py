import logging
from neo4j.exceptions import ServiceUnavailable
from neo4j import GraphDatabase
db = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "lucas041203"))
session = db.session()

# query = """ MATCH (p:Person) RETURN p"""
# results = session.run(query)
# for i in results:
#     print(i) 

def create_node_tx(tx, name):
    result = tx.run("CREATE (n:Usuario { name: $name }) RETURN id(n) AS node_id", name=name)
    record = result.single()
    return record["node_id"]

def _create_and_return_friendship(tx, person1_name, person2_name):
        # To learn more about the Cypher syntax, see https://neo4j.com/docs/cypher-manual/current/
        # The Reference Card is also a good resource for keywords https://neo4j.com/docs/cypher-refcard/current/
        query = (
            "MATCH (p1:Usuario { name: $person1_name }) "
            "MATCH (p2:Usuario { name: $person2_name }) "
            "MERGE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": row["p1"]["name"], "p2": row["p2"]["name"]}
                    for row in result]
        # Capture any errors along with the query and data for traceability
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

with session:
    node_id = session.write_transaction(create_node_tx, "Rubens")
    node_id1 = session.write_transaction(create_node_tx, "Higor")
    node_id2 = session.write_transaction(create_node_tx, "Davi")
    node_id3 = session.write_transaction(create_node_tx, "Marilia")
    node_id3 = session.write_transaction(create_node_tx, "Neusa")
    node_id4 = session.write_transaction(_create_and_return_friendship,"Marilia", "Neusa")