import torch
from flask import Flask, render_template, request

def evaluate(path):

    model = torch.hub.load('/Users/adriantanko/JupyterNotebooks/InnoWeek/yolov5', 'custom', path='/Users/adriantanko/JupyterNotebooks/InnoWeek/yolov5/runs/train/exp/weights/best.pt', source='local')

    # Evaluate
    results = model(path)
    results.save()

    #return results.pandas().xyxy[0].to_json(orient="records")
    return render_template('upload.html', path='runs/detect/exp/enzo.jpg')