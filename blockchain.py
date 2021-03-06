from werkzeug.wrappers import Request, Response
from flask import Blueprint, request
import settings
import subprocess

blockchain = Blueprint('blockchain', __name__)

@blockchain.route(settings.version + '/blockchain' , methods = ['OPTIONS'])
def uselessFunction():
    rsp = Response("")
    rsp.headers['Access-Control-Allow-Origin']='*'
    rsp.headers['Access-Control-Max-Age'] = 3628800
    rsp.headers['Access-Control-Allow-Methods'] = 'POST, DELETE'
    rsp.headers['Access-Control-Allow-Headers'] = 'content-type' 
    return rsp

@blockchain.route(settings.version + '/blockchain' , methods = ['POST'])
def createChain():
    parameter = request.get_json()
    settings.updateChainName(parameter['chainName'])
    # to verify if some of the params received are in the default params
    command = (
        [settings.pathToMultichain + "/multichain-util"]
        + [ "create" , settings.chainName] 
        + parameter['params'] 
        + settings.defaultBlockchainParamsList
        )
    output = subprocess.Popen(command, stdout=subprocess.PIPE).communicate()[0]
    return settings.corsResponse(output)

@blockchain.route(settings.version + '/blockchain' , methods = ['DELETE'])
def destroyChain():
    if settings.nodePid == 0:
        command = ["rm", "-r" , settings.pathToHiddenMultichain + "/" + settings.chainName] 
        subprocess.call(command)
        return settings.corsResponse(settings.chainName + " deleted.")
    else:
        return settings.corsResponse("Stop the connection before deleting the chain!")
    
    