from fastapi import FastAPI, HTTPException

from app.laptop import Laptop, CreateLaptopModel
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

laptops: list[Laptop] = [
    # Laptop(0, 'Lenovo', 'Hong Kong(China)'),
    # Laptop(1, 'HP', 'United States'),
    # Laptop(2, 'Dell', 'United States'),
    # Laptop(3, 'Apple', 'United States'),
    # Laptop(4, 'Walton', 'Bangladesh	')
]


def add_laptops(content: CreateLaptopModel):
    id = len(laptops)
    laptops.append(Laptop(id, content.model, content.developer))
    return id


app = FastAPI()


###############
# Jaeger

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    SERVICE_NAME: "phones-service"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

#
###############

###############
# Prometheus

from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#
###############


@app.get("/v1/laptops")
async def get_laptop():
    return laptops


@app.post("/v1/laptops")
async def add_laptop(content: CreateLaptopModel):
    add_laptops(content)
    return laptops[-1]


@app.get("/v1/laptops/{id}")
async def get_laptop_by_id(id: int):
    result = [item for item in laptops if item.id == id]
    if len(result) > 0:
        return result[0]
    raise HTTPException(status_code=404, detail="Laptop not found")


@app.get("/__health")
async def check_service():
    return
