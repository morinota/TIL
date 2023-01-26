import * as http from "http";
import { fortune, port } from "./config";

// httpサーバーを設定する
const server = http.createServer(
  (request: http.IncomingMessage, response: http.ServerResponse) => {
    // サーバーにリクエストがあった時に実行される関数
    response.end("OK");
  }
);
// サーバーを起動してリクエストを待ち受け状態にする
server.listen(port);
// ログを出力する
console.log(`http://localhost:${port} へアクセスください:${fortune()}`);

