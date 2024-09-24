from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Simula um banco de dados em memória
data_store = [
    {'id': 1, 'name': 'Item 1', 'description': 'Description for Item 1'},
    {'id': 2, 'name': 'Item 2', 'description': 'Description for Item 2'}
]

# Função para buscar um item pelo ID
def find_item(item_id):
    return next((item for item in data_store if item['id'] == item_id), None)

# GET: Retorna todos os itens
@app.route('/api/items', methods=['GET'])
def get_items():
    """
    Retorna todos os itens da loja.
    ---
    responses:
      200:
        description: Uma lista de itens.
        schema:
          type: object
          properties:
            items:
              type: array
              items:
                type: object
                properties:
                  id:
                    type: integer
                    example: 1
                  name:
                    type: string
                    example: "Item 1"
                  description:
                    type: string
                    example: "Description for Item 1"
    """
    return jsonify({'items': data_store})

# GET: Retorna um item específico
@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    """
    Retorna um item específico pelo ID.
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID do item a ser retornado.
    responses:
      200:
        description: Um único item.
        schema:
          type: object
          properties:
            item:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
      404:
        description: Item não encontrado.
    """
    item = find_item(item_id)
    if item:
        return jsonify({'item': item})
    return jsonify({'error': 'Item not found'}), 404

# POST: Cria um novo item
@app.route('/api/items', methods=['POST'])
def create_item():
    """
    Cria um novo item.
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          required:
            - name
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      201:
        description: Item criado com sucesso.
        schema:
          type: object
          properties:
            item:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
      400:
        description: Requisição inválida.
    """
    if not request.json or not 'name' in request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    new_item = {
        'id': data_store[-1]['id'] + 1 if data_store else 1,
        'name': request.json['name'],
        'description': request.json.get('description', '')
    }
    data_store.append(new_item)
    return jsonify({'item': new_item}), 201

# PUT: Atualiza um item existente
@app.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    """
    Atualiza um item existente.
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID do item a ser atualizado.
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
            description:
              type: string
    responses:
      200:
        description: Item atualizado com sucesso.
        schema:
          type: object
          properties:
            item:
              type: object
              properties:
                id:
                  type: integer
                name:
                  type: string
                description:
                  type: string
      404:
        description: Item não encontrado.
      400:
        description: Requisição inválida.
    """
    item = find_item(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    if not request.json:
        return jsonify({'error': 'Bad request'}), 400
    
    item['name'] = request.json.get('name', item['name'])
    item['description'] = request.json.get('description', item['description'])
    return jsonify({'item': item})

# DELETE: Remove um item
@app.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Remove um item.
    ---
    parameters:
      - name: item_id
        in: path
        type: integer
        required: true
        description: ID do item a ser removido.
    responses:
      200:
        description: Item deletado com sucesso.
      404:
        description: Item não encontrado.
    """
    item = find_item(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data_store.remove(item)
    return jsonify({'result': 'Item deleted'})

if __name__ == '__main__':
    app.run(debug=True)
