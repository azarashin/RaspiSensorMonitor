# このソフトでできること

- grove ３軸加速度センサの状態をI2C 通信で取得する
- WebAPI によりセンサの状態をクライアントへ送信する


# 準備

## モジュールインストール

pip3 install -r requirements.txt

## ファイアウォール設定

サーバのIPアドレスとポート番号を決めておく。
この説明ではサーバのアドレスを192.168.0.100, ポート番号を8000 とする。
下記のコマンドを実行し、ファイアウォールを有効にしておく。

```
sudo apt install ufw
sudo ufw enable
sudo ufw allow 8000
sudo ufw reload
sudo ufw status
```

sudo ufw status を実行したときに開放したポート番号のアクセス許可が
表示されるのを確認する。


もしufw の実行時に下記のエラーが出た場合

```
$ sudo ufw allow 80
ERROR: Couldn't determine iptables version
```

iptables のバージョンが古い場合があるので、iptables をインストールしなおしてみる。

```
sudo apt install iptables
```
