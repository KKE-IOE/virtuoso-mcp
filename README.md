# Virtuoso SPARQL MCP Server

Virtuoso SPARQL MCP Serverは、SPARQLクエリをVirtuosoエンドポイントに送信し、結果を取得するためのMCP（Model Context Protocol）サーバーです。ClineやClaude Desktopなどのツールから、SPARQLクエリを実行するために使用できます。

## 機能

- SPARQLクエリをVirtuosoエンドポイントに送信
- 複数の結果フォーマット（JSON、XML、CSV、TSV）をサポート
- ClineやClaude Desktopとの統合

## インストール方法

### 前提条件

- Python 3.8以上
- pip（Pythonパッケージマネージャー）

### 手順

1. リポジトリをクローンまたはダウンロードします。

```bash
git clone https://github.com/yourusername/virtuoso-mcp.git
cd virtuoso-mcp
```

2. 必要なライブラリをインストールします。

```bash
pip install SPARQLWrapper mcp anyio click
```

3. MCPサーバーの設定を行います。

#### Clineの場合

Clineの設定ファイルは通常、以下の場所にあります：
- Windows: `C:\Users\<ユーザー名>\AppData\Roaming\Code\User\globalStorage\saoudrizwan.claude-dev\settings\cline_mcp_settings.json`
- macOS: `~/Library/Application Support/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`
- Linux: `~/.config/Code/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

このファイルに以下の設定を追加します（既存の設定がある場合は、`mcpServers`オブジェクト内に追加します）：

```json
{
  "mcpServers": {
    "virtuoso-mcp": {
      "command": "python",
      "args": ["<virtuoso_server.pyへのフルパス>"],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

`<virtuoso_server.pyへのフルパス>`は、実際のファイルパスに置き換えてください。例：`"e:/git/virtuoso-mcp/virtuoso_server.py"`

#### Claude Desktopの場合

Claude Desktopの設定ファイルは通常、以下の場所にあります：
- Windows: `C:\Users\<ユーザー名>\AppData\Roaming\Claude Desktop\mcp_settings.json`
- macOS: `~/Library/Application Support/Claude Desktop/mcp_settings.json`
- Linux: `~/.config/Claude Desktop/mcp_settings.json`

このファイルに以下の設定を追加します：

```json
{
  "mcpServers": {
    "virtuoso-mcp": {
      "command": "python",
      "args": ["<virtuoso_server.pyへのフルパス>"],
      "disabled": false,
      "alwaysAllow": []
    }
  }
}
```

## 使用方法

### Clineからの使用

1. VSCodeでCline拡張機能を開きます。
2. MCPサーバーの接続状態を確認します。「virtuoso-mcp」が接続されていることを確認してください。
3. チャットウィンドウで以下のようにSPARQLクエリを実行します：

```
SPARQLクエリを実行してください：

エンドポイント: https://jpsearch.go.jp/rdf/sparql/
クエリ:
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX place: <https://jpsearch.go.jp/entity/place/>
PREFIX type: <https://jpsearch.go.jp/term/type/>
SELECT ?s ?label WHERE {
    ?s schema:spatial place:三重 ;
        rdfs:label ?label ;
        a type:陶磁 .
}
```

### Claude Desktopからの使用

1. Claude Desktopを起動します。
2. MCPサーバーの接続状態を確認します。「virtuoso-mcp」が接続されていることを確認してください。
3. チャットウィンドウで以下のようにSPARQLクエリを実行します：

```
SPARQLクエリを実行してください：

エンドポイント: https://jpsearch.go.jp/rdf/sparql/
クエリ:
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX place: <https://jpsearch.go.jp/entity/place/>
PREFIX type: <https://jpsearch.go.jp/term/type/>
SELECT ?s ?label WHERE {
    ?s schema:spatial place:三重 ;
        rdfs:label ?label ;
        a type:陶磁 .
}
```

## SPARQLクエリの例

### 三重県に関連する陶磁器のリストを取得

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
PREFIX place: <https://jpsearch.go.jp/entity/place/>
PREFIX type: <https://jpsearch.go.jp/term/type/>
SELECT ?s ?label WHERE {
    ?s schema:spatial place:三重 ;
        rdfs:label ?label ;
        a type:陶磁 .
}
```

### 特定のキーワードを含む資料を検索

```sparql
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX schema: <http://schema.org/>
SELECT ?s ?label WHERE {
    ?s rdfs:label ?label .
    FILTER(CONTAINS(?label, "色絵"))
}
LIMIT 10
```

## トラブルシューティング

### MCPサーバーに接続できない場合

1. 設定ファイルのパスが正しいことを確認してください。
2. 必要なライブラリがインストールされていることを確認してください。
3. ログファイル（`virtuoso_server_log.txt`）を確認して、エラーメッセージを確認してください。

### SPARQLクエリの実行中にエラーが発生する場合

1. エンドポイントURLが正しいことを確認してください。
2. クエリの構文が正しいことを確認してください。
3. エンドポイントがアクセス可能であることを確認してください。

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。詳細については、[LICENSE](LICENSE)ファイルを参照してください。
