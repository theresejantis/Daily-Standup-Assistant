import logging

from opentelemetry import trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.sdk.resources import Resource

from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor

from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter

from openinference.instrumentation.groq import GroqInstrumentor


resource = Resource.create(
    {
        "service.name": "daily-standup-assistant"
    }
)


trace_provider = TracerProvider(resource=resource)

trace_provider.add_span_processor(
    BatchSpanProcessor(
        OTLPSpanExporter(
            endpoint="localhost:18889",
            insecure=True
        )
    )
)

trace.set_tracer_provider(trace_provider)

tracer = trace.get_tracer("daily-standup-assistant")


log_provider = LoggerProvider(resource=resource)

log_provider.add_log_record_processor(
    BatchLogRecordProcessor(
        OTLPLogExporter(
            endpoint="localhost:18889",
            insecure=True
        )
    )
)

set_logger_provider(log_provider)

logger = logging.getLogger("daily-standup-assistant")
logger.setLevel(logging.INFO)

logger.addHandler(
    LoggingHandler(
        logger_provider=log_provider
    )
)


GroqInstrumentor().instrument()

print("Telemetry Initialized")