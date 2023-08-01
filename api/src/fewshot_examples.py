def get_fewshot_examples(openai_api_key):
    return f"""
#How is user ShaunSHamilton connected to user ojeytonwilliams?
MATCH (u1:User {{login:"ShaunSHamilton"}}), (u2:User {{login:"ojeytonwilliams"}})
MATCH p=shortestPath((u1)-[*]-(u2))
RETURN p
#How many organisations are there in the graph?
MATCH (o:Organisation) RETURN count(o)
#Which projects does freeCodeCamp have?
MATCH (o:Organisation {{name:"freeCodeCamp"}})-[:HAS_PROJECT]-(p:Project) RETURN count(DISTINCT p)
#Which repositories are affected by freeCodeCamp's project Backend API?
MATCH (:Organisation {{name:"freeCodeCamp"}})-[:HAS_PROJECT]-(p:Project {{title: "Backend API"}})
MATCH (p)-[:CONTAINS]-(:Issue)-[:CONTAINS]-(r:Repository)
RETURN DISTINCT r
#Which users are assigned to freeCodeCamp's issue "GET /user/get-session-user"?
MATCH (:Organisation {{name:"freeCodeCamp"}})-[:HAS_PROJECT]-(:Project)-[:CONTAINS]-(i:Issue {{title: "GET /user/get-session-user"}})-[:HAS_EVENT]-(ae:AssignedEvent)-[:ASSIGNED_TO]-(u:User)
WHERE NOT EXISTS {{
  MATCH (i)-[:HAS_EVENT]-(ue:UnassignedEvent)-[:ASSIGNED_TO]-(u) 
  WHERE ue.createdAt > ae.createdAt
}}
RETURN DISTINCT u
#Which users were assigned to electron's issue numbeer 39000 but are not assigned to it anymore?
MATCH (:Organisation {{name:"electron"}})-[:HAS_PROJECT]-(:Project)-[:CONTAINS]-(i:Issue {{number: 39000}})-[:HAS_EVENT]-(ae:AssignedEvent)-[:ASSIGNED_TO]-(u:User)
WHERE EXISTS {{
  MATCH (i)-[:HAS_EVENT]-(ue:UnassignedEvent)-[:ASSIGNED_TO]-(u) 
  WHERE ue.createdAt > ae.createdAt
  AND NOT EXISTS {{
    MATCH (i)-[:HAS_EVENT]-(ae2:AssignedEvent)-[:ASSIGNED_TO]-(u) 
    WHERE ae2.createdAt > ue.createdAt
  }}
}}
RETURN DISTINCT u
#Which issues are closed?
MATCH (i:Issue)-[:HAS_EVENT]-(:ClosedEvent) RETURN DISTINCT i
#Which users closed electron's issue 39077?
MATCH (:Organisation {{name:"electron"}})-[:HAS_PROJECT]-(:Project)-[:CONTAINS]-(i:Issue {{number: 39000}})-[:HAS_EVENT]-(ae:AssignedEvent)-[:ASSIGNED_TO]-(u:User),
(i)-[:HAS_EVENT]-(:ClosedEvent)
WHERE NOT EXISTS {{
  MATCH (i)-[:HAS_EVENT]-(ue:UnassignedEvent)-[:ASSIGNED_TO]-(u) 
  WHERE ue.createdAt > ae.createdAt
}}
RETURN DISTINCT u
"""
