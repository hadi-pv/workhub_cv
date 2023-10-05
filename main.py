import shutil
import uvicorn
import TableExtractor as te
import TableLinesRemover as tlr
import OcrToTableTool as ottt
from fastapi import FastAPI,File, UploadFile

app=FastAPI()

@app.post("/")
async def root(image: UploadFile = File(...)):
    path_to_image = "./input/"+image.filename
    try:
        with open(path_to_image, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
    except:
        return "Error in uploading image"
    table_extractor = te.TableExtractor(path_to_image)
    perspective_corrected_image = table_extractor.execute()

    lines_remover = tlr.TableLinesRemover(perspective_corrected_image)
    image_without_lines = lines_remover.execute()

    ocr_tool = ottt.OcrToTableTool(image_without_lines, perspective_corrected_image)

    return {"result":ocr_tool.execute(),"filename":path_to_image}
    
    
if __name__ == "__main__":
  uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)