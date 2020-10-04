import uuid

from ariadne import QueryType, graphql_sync, make_executable_schema, \
    MutationType, snake_case_fallback_resolvers, convert_kwargs_to_snake_case
from ariadne.constants import PLAYGROUND_HTML
from flask import Flask, request, jsonify


TODOS = [
    {
        "id": "2882u32joijd292",
        "description": "Do some gardening",
        "completed": False,
        "due_date": 1601845200.0
    },
    {
        "id": "6318132joijd292",
        "description": "Shopping",
        "completed": False,
        "due_date": 1601758800.0
    },
    {
        "id": "7168127616joijd292",
        "description": "File taxes",
        "completed": False,
        "due_date": 1601758800.0
    }
]

type_defs = """
  type Todo {
    id: ID!
    description: String!
    completed: Boolean!
    dueDate: Float!
  }

  type Query {
    todos: [Todo]!
    todo(todoId: ID!): Todo
  }
  
  input TodoInput {
    description: String!, 
    dueDate: Float!
  }

  type Mutation {
    createTodo(input: TodoInput!): Todo!
    deleteTodo(todoId: ID!): String!
   }
"""

query = QueryType()
mutation = MutationType()


@convert_kwargs_to_snake_case
@query.field("todos")
def resolve_todos(obj, info):
    return TODOS


@mutation.field("createTodo")
@convert_kwargs_to_snake_case
def resolve_create_todo(obj, info, input):
    todo_input = {
        "description": input.get("description"),
        "due_date": input.get("due_date"),
        "completed": False,
        "id": str(uuid.uuid4())
    }
    TODOS.append(todo_input)
    return todo_input


schema = make_executable_schema(
    type_defs, [query, mutation], snake_case_fallback_resolvers
)

app = Flask(__name__)


@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()

    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == '__main__':
    app.run(debug=True)
