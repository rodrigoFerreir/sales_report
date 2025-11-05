import json
import logging
from typing import Dict, Any
from output.formatters.formater_contract import IFormater
from decimal import Decimal

logger = logging.getLogger(__name__)


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            return str(o)
        return super().default(o)


class JsonFormater(IFormater):
    def execute(self, report_data: Dict[str, Any]) -> str:
        try:
            return json.dumps(
                report_data, indent=4, ensure_ascii=False, cls=DecimalEncoder
            )
        except Exception as err:
            logger.error(f"Erro ao formatar dados do relatorio no fomato json {err}")
            return ""
