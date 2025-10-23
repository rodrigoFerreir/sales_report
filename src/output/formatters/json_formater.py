import json
import logging
from typing import Dict, Any
from output.formatters.formater_contract import IFormater

logger = logging.getLogger(__name__)


class JsonFormater(IFormater):
    def execute(self, report_data: Dict[str, Any]) -> str:
        try:
            return json.dumps(report_data, indent=4, ensure_ascii=False)
        except Exception as err:
            logger.error(f"Erro ao gerar relatorio no fomato json {err}")
            return ""
