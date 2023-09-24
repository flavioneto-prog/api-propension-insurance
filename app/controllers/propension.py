from flask import Response
from flask_restx import Resource, Namespace
import tensorflow_decision_forests as tfdf
import numpy as np
import pandas as pd
import tensorflow as tf

namespace = Namespace("propensions" , description="Obter propensão de seguros de acordo com perfil do cliente.")

modelo = tf.keras.models.load_model("modelo")

@namespace.route("/propensions/<int:age>/<string:sex>/<string:profission>/<int:income>")
class PropesionAPI(Resource):
    
    def get(self, age, sex, profission, income):
        
        if income <= 0:
            return 'Idade do cliente fora do range permitido para contratação do seguro', 400

        if  18 >= age > 60:
            return 'Idade do cliente fora do range permitido para contratação do seguro', 400

        if sex not in ('Masculino', 'Feminino'):
            return "Sexo informado inválido, tente nos formatos (Masculino ou Feminino)", 400
        
        predict = modelo.predict({
            "idade": np.array([age]),
            "sexo": np.array([sex]),
            "profissao": np.array([profission]),
            "renda": np.array([income]),
        })[:1]

        classes = ['Vida Familia', 'Carro', 'Fatura Protegida', 'Proteção Pessoal', 'Moto', 'Celular']
        scores = list(zip(predict[0].tolist(), (classes)))
        scores = [{"insurance": y, "score": x} for x, y in scores]
        scores.sort(reverse = True, key = lambda x : x['score'])

        return scores, 200