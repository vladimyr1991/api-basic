import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import Literal
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.encoders import jsonable_encoder
from data_processing import DataProcessing
from fastapi.openapi.utils import get_openapi
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")

dp = DataProcessing()



def my_schema():
    openapi_schema = get_openapi(
        title="API for Veyt assesment",
        version="1.0",
        routes=app.routes,
        )
    openapi_schema["info"] = {
        "description": """<b>Task description</b>
                        \nBuild a RESTful API with Python (FastAPI) and deploy it to fly.io (It is free cloud service)
                        \nUse the dataset below: <href>https://github.com/GreenfactAS/co2-dataset</href>
                        \nThe api should return:
                        \n1. Top 10 Countries with highest Co2Emissions perCapita
                        \n2. Return CO2Emissions and YearlyChange given a list of country codes (Ex,: can,lux,est)
                        \n3. Top 10 Countries with highest LifeExpectancy
                        \n4. Total of Emissions given a list of countries codes (Ex,: can,lux,est)""",
        "contact": {
                     "name": "Get Help with this API",
                     "email": "vladimir.moroz.a@yandex.com"
                     },
        }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = my_schema


class ParameterRequest(BaseModel):
    statistics_type: Literal[1, 2, 3, 4, "1", "2", "3", "4"]
    country_codes: list[str] = None

    class Config:
        schema_extra = {
            "example": {
                "statistics_type": "2",
                "country_codes": ["can", "lux", "est"]
                }
            }


@app.get("/", tags=["Methods"], include_in_schema=False)
async def main(request: Request):
    context = {"request": request}
    return templates.TemplateResponse("index.html", context)


@app.get("/healthcheck", tags=["Methods"], include_in_schema=False)
def read_root():
    return {"status": "ok"}


@app.post("/calculateStatistics", tags=["Methods"])
def calculate_statistics(parameters: ParameterRequest):
    """
    <b>statistics_type:</b> id of statistics from 1 to 4 in accordance with the technical task

    <b>country_codes:</b> list with country code(s) (Ex,: ["can","lux","est"]) or null if method is not required
    """

    statistics_type = int(parameters.statistics_type)
    data = {}

    if statistics_type == 1 or statistics_type == 3:
        if not parameters.country_codes:

            # 1. Top 10 Countries with highest Co2Emissions per Capita
            if statistics_type == 1:
                key = "top_10_countries_with_highest_co2_emission_per_capita"

            # 3. Top 10 Countries with highest LifeExpectancy
            elif statistics_type == 3:
                key = "top_10_countries_with_highest_life_expectancy"

            value = dp.calculate_statistics(statistics_type=statistics_type)
            data[key] = value
        else:
            content = {"message": "when requesting statistics_type 1 or 3  do not define 'country_codes' key at all or set its value equal to 'null' "}
            return JSONResponse(status_code=400, content=content)

    elif statistics_type == 2 or statistics_type == 4:
        if parameters.country_codes:
            if statistics_type == 2:
                key = "co2_emissions_and_yearly_change"
            elif statistics_type == 4:
                key = "total_of_emissions"

            value = dp.calculate_statistics(statistics_type=statistics_type, country_codes=parameters.country_codes)

            if value != "code misspell error":
                data[key] = value
            else:
                content = {
                    "message": "Some of country codes are incorrect or does not exist in database, please check codes",
                    "info": {"list_of_available_country_codes": dp.country_codes}
                    }
                return JSONResponse(status_code=400, content=content)
        else:
            content = {"message": "When specifying statistic_type 2 or 4 you should specify 'country_codes' in a list Ex,: ['can','lux','est']"}
            return JSONResponse(status_code=400, content=content)

    return JSONResponse(content=jsonable_encoder(data))
