from    fastapi                 import FastAPI
from    fastapi.middleware.cors import CORSMiddleware
from    pydantic                import BaseModel
import  ctypes
app     = FastAPI()

#mode de dado esperado
class DadosRegex(BaseModel):
    string: str
    regex: str

#estrutura de dados que o C retorna ao python
class ResultadoRegex (ctypes.Structure):
    _fields_ = [("aceito",ctypes.c_int),
                ("posicao",ctypes.c_int),
                ("caractere",ctypes.c_char) ]

#Adciona um middler para filtrar as conexões
app.add_middleware(CORSMiddleware, 
    allow_origins=["*"],                #lista que permite especificar o IP de quem pode conecar a api.
    allow_methods=["POST"],             #lista que permite especificar os metodos aceitos pela api.
    allow_headers=["Content-Type"]      #lista que permite especifar os headers uma requisição no CORS pode enviar
    )                


#carrega o codigo C na memoria
motor_regex = ctypes.CDLL("./libmotor_regex.so")

#define a assinatura da função do motor para dois ponteiros char (um para a string e outro para o regex)
motor_regex.MotorRegex.argtypes             = [ctypes.c_char_p, ctypes.c_char_p]

#define a assinatura da função que libera a memoria do resultado do regex
motor_regex.LiberarResultado.argtypes   = [ctypes.POINTER (ResultadoRegex)]

#define o retorno da função do motor regex como sendo  um ponteiro para uma estrutura 
motor_regex.MotorRegex.restype      = ctypes.POINTER (ResultadoRegex)

#Define a api do motor regex
@app.post("/motor_regex")
def MotorRegex(dados: DadosRegex):

    #converte as strings para ponteiros C
    ptr_string = ctypes.c_char_p(dados.string.encode())
    ptr_regex  = ctypes.c_char_p(dados.regex.encode())

    #chama o motor regex
    resultado = motor_regex.MotorRegex( ptr_string, ptr_regex )

    #verifica se NULL
    if not resultado:
     return { 
        "status" : "erro de back end",
        "posicao" : -1,
        "caractere": -1
        }
    

    #obtem  os campos da estrutura
    status      = resultado.contents.aceito
    posicao     = resultado.contents.posicao                     
    caractere   = resultado.contents.caractere.decode()          #ctypes converte char para byte. Por isso requer decode

    #libera  a memoria do regex
    motor_regex.LiberarResultado(resultado)

    #trata o retorno
    if status ==  0:
        return {
        "status"    : f"Match: {dados.string}",
        "posicao"   :0,
        "caractere" :0
        }
    else:
        return { 
        "status" : "falha",
        "posicao" : posicao,
        "caractere": caractere
        }
    