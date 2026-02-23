from neo4j import GraphDatabase
import os
import json
from datetime import datetime

class Neo4jClient:
    def __init__(self):
        uri = os.getenv("NEO4J_URL_ENDPOINT")
        user = os.getenv("NEO4J_USERNAME")
        password = os.getenv("NEO4J_PASSWORD")
        
        if uri and user and password:
            print(f"🕸️ Connecting to Neo4j: {uri}...")
            try:
                self.driver = GraphDatabase.driver(uri, auth=(user, password))
                self.verify_connection()
            except Exception as e:
                print(f"❌ Neo4j Connection Failed: {e}")
                self.driver = None
        else:
             print("⚠️ Missing Neo4j Credentials in .env")
             self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def verify_connection(self):
        with self.driver.session() as session:
            result = session.run("RETURN 1 AS num")
            record = result.single()
            if record and record["num"] == 1:
                print("✅ Neo4j Connection Verified!")
            else:
                 print("❌ Neo4j Verification Failed.")

    def store_summary_intelligence(self, summary_text: str, metadata: dict, entities: list):
        """
        Stores the Summary, Source User, and Extracted Entities relationship in the Graph.
        
        Graph Schema:
        (User:User) -[WROTE]-> (Summary:Summary)
        (Summary) -[MENTIONS]-> (Issue:Issue)
        (Summary) -[MENTIONS]-> (Feature:Feature)
        """
        if not self.driver:
            return

        with self.driver.session() as session:
            session.execute_write(self._create_standard_nodes, summary_text, metadata, entities)

    @staticmethod
    def _create_standard_nodes(tx, summary_text, metadata, entities):
        # 1. Create/Merge User Node
        user_id = metadata.get("User") or metadata.get("user") or "Anonymous"
        tx.run(
            """
            MERGE (u:User {id: $user_id})
            RETURN u
            """,
            user_id=user_id
        )

        # 2. Create Summary Node (Linked to User)
        # Using a hash or timestamp for ID if not provided
        summary_id = f"summ_{hash(summary_text)}"
        tx.run(
            """
            MATCH (u:User {id: $user_id})
            CREATE (s:Summary {
                id: $summary_id, 
                text: $text, 
                timestamp: $timestamp
            })
            CREATE (u)-[:WROTE]->(s)
            """,
            user_id=user_id,
            summary_id=summary_id,
            text=summary_text,
            timestamp=datetime.now().isoformat()
        )

        # 3. Create Entity Nodes & Edges
        for entity in entities:
            # entity = {'name': 'Battery Life', 'type': 'Issue', 'sentiment': 'Negative'}
            label = entity.get("type", "Entity").capitalize() # e.g., Issue, Feature
            name = entity.get("name", "Unknown")
            sentiment = entity.get("sentiment", "Neutral")
            
            # Sanitize Label (Cyber injection prevention - basic)
            allowed_labels = ["Issue", "Feature", "Product", "Sentiment"]
            if label not in allowed_labels:
                label = "Entity"

            # Merge Entity Node (e.g., (i:Issue {name: 'Battery Life'}))
            query = f"""
            MERGE (e:{label} {{name: $name}})
            """
            tx.run(query, name=name)

            # Link Summary -> Entity
            # (s)-[:MENTIONS {sentiment: 'Negative'}]->(e)
            link_query = f"""
            MATCH (s:Summary {{id: $summary_id}})
            MATCH (e:{label} {{name: $name}})
            CREATE (s)-[:MENTIONS {{sentiment: $sentiment}}]->(e)
            """
            tx.run(link_query, summary_id=summary_id, name=name, sentiment=sentiment)

        print(f"🕸️ Graph Updated: 1 Summary, {len(entities)} Entities linked.")
