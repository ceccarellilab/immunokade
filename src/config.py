import os

path_project = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


path_input = path_project+os.sep+"data_input"
path_output = path_project+os.sep+"data_output"

path_hla_pocket = path_project+os.sep+"src"+os.sep+"hla_pocket.csv"

tokens_len = 15+34+15

path_model_ik_f1 = path_project+os.sep+"models"+os.sep+"CV1"+os.sep+"cv1_model_trained.pth"
path_model_ik_f2 = path_project+os.sep+"models"+os.sep+"CV2"+os.sep+"cv2_model_trained.pth"
path_model_ik_f3 = path_project+os.sep+"models"+os.sep+"CV3"+os.sep+"cv3_model_trained.pth"
path_model_ik_f4 = path_project+os.sep+"models"+os.sep+"CV4"+os.sep+"cv4_model_trained.pth"
path_model_ik_f5 = path_project+os.sep+"models"+os.sep+"CV5"+os.sep+"cv5_model_trained.pth"

