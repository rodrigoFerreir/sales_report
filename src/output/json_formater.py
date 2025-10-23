import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)


class JsonFormater:

    @staticmethod
    def execute(report_data: Dict[str, Any]) -> str:
        try:
            return json.dumps(report_data, indent=4, ensure_ascii=False)
        except Exception as err:
            logger.error(f"Erro ao gerar relatorio no fomato json {err}")
