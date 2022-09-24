import json

import boto3
import json

client = boto3.client('rekognition')
s3 = boto3.resource('s3')


#Este metodo Faz a detecção de faces das imagens do  bucket
def detecta_faces():
    faces_detectadas = client.index_faces(
        CollectionId='faces',
        DetectionAttributes=['DEFAULT'],
        ExternalImageId='TEMPORARIA',
        Image={
            'S3Object': {
                'Bucket': 'faimagem',
                'Name': '_ANALISE.png',
            },
        },
    )

    return faces_detectadas


#Este Método cria uma lista com todas as faces detectadas nas imagens
def cria_lista_faceId_detectadas(faces_detectadas):
    faceId_detectadas = []
    for imagens in range(len(faces_detectadas['FaceRecords'])):
        faceId_detectadas.append(faces_detectadas['FaceRecords'][imagens]['Face']['FaceId'])
    return faceId_detectadas


#Este Metodo faz a comparação entre as imagens no bucket e a nova imagem adicionada
def compara_imagens(faceId_detectadas):
    resultado_comparacao = []
    for ids in faceId_detectadas:
        resultado_comparacao.append(
            client.search_faces(
                CollectionId='faces',
                FaceId=ids,
                FaceMatchThreshold=80,
                MaxFaces=10,
            )
        )
    return resultado_comparacao

# Este Método faz uma triagem do resultado da comparação
def gera_dados_json(resultado_comparacao):
    dados_json = []
    for face_matches in resultado_comparacao:
        if(len(face_matches.get('FaceMatches'))) >=1:
            perfil = dict(nome=face_matches['FaceMatches'][0]['Face']['ExternalImageId'],
                          faceMatch=round(face_matches['FaceMatches'][0]['Similarity'], ))
            dados_json.append(perfil)
    return dados_json

#Este Método publica os dados no Bucket que contem o site
def publica_dados(dados_json):
    arquivo = s3.Object('fasite', 'dados.json')
    arquivo.put(Body=json.dumps(dados_json))

# Este Método exclui a imagem adicionada para a Comparação
def exclui_imagem_colecao(faceId_detectadas):
    client.delete_faces(
        CollectionId='faces',
        FaceIds=faceId_detectadas,
    )

# Este Método chama todos os métodos
def main():
    faces_detectadas = detecta_faces()
    faceId_detectadas = cria_lista_faceId_detectadas(faces_detectadas)
    resultado_comparacao = compara_imagens(faceId_detectadas)
    dados_json = gera_dados_json(resultado_comparacao)
    publica_dados(dados_json)
    exclui_imagem_colecao(faceId_detectadas)
    print(json.dumps(dados_json, indent=4))

main()