了解です。
**「Debian + GNOME + IBus で地雷を踏まない最小・正規手順」**を
**実行順そのまま**でまとめます。
（理由説明は最小限、手順は安全側のみ）

---

# 前提（守ること）

* **ユーザー領域は使わない**
* **IBus を手動起動・再起動しない**
* **環境変数 `IBUS_COMPONENT_PATH` は使わない**
* 反映は **再ログイン**で行う

---

# ゴール

* 自前 IBus エンジンを Debian に安全に登録
* Mozc を壊さない
* `ibus list-engine` に出る

---

## ステップ1：エンジン本体をシステムに配置

```bash
sudo install -m 755 \
  ibus-engine-sample.py \
  /usr/libexec/ibus-engine-sample

# for re-install
# pkill -f ibus-engine-sample
```

確認：

```bash
ls -l /usr/libexec/ibus-engine-sample
tail -f /tmp/ibus-sample.log
```

---

## ステップ2：component XML を配置

### XML の必須条件

* `<exec>` は **絶対パス**
* engine 名は **短く一意**
* 空要素を作らない（GLib 警告回避）

### 例（重要部分だけ）

```xml
<exec>/usr/libexec/ibus-engine-sample</exec>
```

### 配置

```bash
sudo install -m 644 \
  sample.xml \
  /usr/share/ibus/component/sample.xml
```

---

## ステップ3：IBus のキャッシュを更新（ここだけ sudo）

```bash
sudo ibus write-cache
```

※ **restart しない**

---

## ステップ4：必ずログアウト → ログイン

これが **正規の反映方法**。

---

## ステップ5：登録確認（初めて触る）

```bash
ibus list-engine | grep sample
```

* 出る → 成功
* 出ない → 次へ

---

## ステップ6：registry に入っているか（確認用）

```bash
ibus read-cache | grep -A5 sample
```

---

## ステップ7：実際に使ってみる（任意）

```bash
ibus engine sample
```

---

# やってはいけない操作（重要）

| 操作                    | 理由            |
| --------------------- | ------------- |
| `ibus restart`        | GNOME 管理と衝突   |
| `ibus-daemon -drx`    | 手動起動で壊す       |
| `IBUS_COMPONENT_PATH` | registry が壊れる |
| user component 常用     | Debian では非推奨  |

---

# トラブル時の唯一の復旧手順

```bash
im-config -n ibus
logout
```

---

## これだけ覚えればOK（要点）

* **/usr/libexec**
* **/usr/share/ibus/component**
* **sudo ibus write-cache**
* **再ログイン**

これが **Debian で壊れない唯一のルート**です。

---

次に進むなら：

* `.deb` 化して配布
* Rust 版 engine に置き換え
* GNOME 設定 UI に必ず出す方法

どれにしますか？
