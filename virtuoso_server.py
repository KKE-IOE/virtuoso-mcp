import json
import sys
import os
import click
import platform
import mcp.types as types
from mcp.server.lowlevel import Server
import anyio
import traceback
import datetime

# SPARQLWrapperのインポートを試みる
try:
    from SPARQLWrapper import SPARQLWrapper, JSON, XML, CSV, TSV
    print("SPARQLWrapper successfully imported")
except ImportError as e:
    print(f"Error importing SPARQLWrapper: {e}")
    sys.exit(1)

# ログファイルの設定
log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "virtuoso_server_log.txt")

def log_to_file(message):
    """ログをファイルに出力する"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")

@click.command()
@click.option("--transport", default="stdio", type=click.Choice(["stdio"]), help="Transport type (only stdio supported)")
def main(transport: str) -> int:
    """Run the Virtuoso SPARQL MCP server."""
    app = Server("Virtuoso SPARQL MCP Server")

    @app.call_tool()
    async def execute_sparql(
        name: str = None,
        arguments: dict = None
    ) -> list[types.TextContent | types.EmbeddedResource]:
        """Execute a SPARQL query on a Virtuoso endpoint.

        Args:
            name: Tool name (should be 'query_virtuoso')
            arguments: Dictionary containing the actual arguments
        """
        try:
            log_to_file(f"FUNCTION CALLED: execute_sparql")
            log_to_file(f"Raw input - name: {repr(name)}, arguments: {repr(arguments)}")
            log_to_file(f"DEBUG: Received arguments: {locals()}")

            # nameパラメータに基づいて処理を分岐
            if name == 'query_virtuoso':
                log_to_file(f"Detected query_virtuoso call, will execute SPARQL query")
            else:
                error_message = f"Error: Unknown tool name '{name}'. Available tool is: query_virtuoso"
                log_to_file(error_message)
                return [types.TextContent(type="text", text=error_message)]

            # 引数の処理
            endpoint_url = None
            query = None
            result_format = "json"  # デフォルト値

            if arguments and isinstance(arguments, dict):
                log_to_file(f"DEBUG: Processing arguments dictionary: {arguments}")
                if "endpoint_url" in arguments:
                    endpoint_url = arguments.get("endpoint_url")
                    log_to_file(f"DEBUG: Using endpoint_url from arguments: {endpoint_url}")
                if "query" in arguments:
                    query = arguments.get("query")
                    log_to_file(f"DEBUG: Using query from arguments: {query}")
                if "result_format" in arguments:
                    result_format = arguments.get("result_format")
                    log_to_file(f"DEBUG: Using result_format from arguments: {result_format}")

            # 入力の検証
            if not endpoint_url:
                log_to_file("Error: No endpoint URL provided")
                return [types.TextContent(type="text", text="Error: No endpoint URL provided")]

            if not query:
                log_to_file("Error: No SPARQL query provided")
                return [types.TextContent(type="text", text="Error: No SPARQL query provided")]

            # 結果フォーマットの正規化
            result_format = result_format.lower()
            if result_format not in ["json", "xml", "csv", "tsv"]:
                log_to_file(f"Invalid result format: {result_format}, using default: json")
                result_format = "json"

            # SPARQLWrapperを使用してクエリを実行
            sparql = SPARQLWrapper(endpoint_url)
            sparql.setQuery(query)

            # 結果フォーマットの設定
            if result_format == "json":
                sparql.setReturnFormat(JSON)
            elif result_format == "xml":
                sparql.setReturnFormat(XML)
            elif result_format == "csv":
                sparql.setReturnFormat(CSV)
            elif result_format == "tsv":
                sparql.setReturnFormat(TSV)

            # クエリの実行
            log_to_file(f"Executing SPARQL query on endpoint: {endpoint_url}")
            results = sparql.query().convert()

            # 結果の処理
            if result_format == "json":
                # JSON形式の結果を整形して返す
                formatted_results = json.dumps(results, ensure_ascii=False, indent=2)
                log_to_file(f"Query executed successfully. Result format: {result_format}")
                return [types.TextContent(type="text", text=formatted_results)]
            else:
                # その他の形式はそのまま文字列として返す
                log_to_file(f"Query executed successfully. Result format: {result_format}")
                return [types.TextContent(type="text", text=str(results))]

        except Exception as e:
            traceback_str = traceback.format_exc()
            log_to_file(f"Error in execute_sparql: {traceback_str}")

            return [
                types.TextContent(type="text", text=f"Error: {str(e)}")
            ]

    @app.list_tools()
    async def list_tools() -> list[types.Tool]:
        """List the available tools for this MCP server."""
        return [
            types.Tool(
                name="query_virtuoso",
                description="Execute a SPARQL query on a Virtuoso endpoint",
                inputSchema={
                    "type": "object",
                    "required": ["endpoint_url", "query"],
                    "properties": {
                        "endpoint_url": {
                            "type": "string",
                            "description": "URL of the Virtuoso SPARQL endpoint"
                        },
                        "query": {
                            "type": "string",
                            "description": "SPARQL query to execute"
                        },
                        "result_format": {
                            "type": "string",
                            "description": "Format of the result (json, xml, csv, tsv)",
                            "enum": ["json", "xml", "csv", "tsv"],
                            "default": "json"
                        }
                    }
                }
            )
        ]

    from mcp.server.stdio import stdio_server

    async def arun():
        async with stdio_server() as streams:
            await app.run(
                streams[0], streams[1], app.create_initialization_options()
            )

    anyio.run(arun)
    return 0

if __name__ == "__main__":
    main()
