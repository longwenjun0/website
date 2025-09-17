import express from 'express';
import cors from 'cors';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;
app.use(cors());
app.use(express.json());

// 启动后初始化数据库
function runPythonOnStartup() {
  const pythonProcess = spawn("python", [
    path.join(__dirname, "models", "init_db.py")
  ]);

  pythonProcess.stdout.on("data", (data) => {
    console.log(`Python: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    if (code === 0) {
      console.log("Python script executed successfully!");
    } else {
      console.error(`Python script exited with code ${code}`);
    }
  });
}

// 执行 Python
runPythonOnStartup();

app.post("/api/chat", (req, res) => {
  const { model, text } = req.body;
  // console.log("model:", model);
  // console.log("text:", text);

  if (!text) {
    return res.status(400).json({ error: "No input text provided" });
  }

  const pythonProcess = spawn("python", [
    path.join(__dirname, "models", "run_model.py"),
    model || "gpt-4o",   // 默认 gpt-4o
    text,
  ]);

  let output = "";

  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
    res.status(500).json({ error: data.toString() });
  });

  // console.log("python output:", output.trim());

  // Python 执行完成后，将结果返回前端
  pythonProcess.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script error" });
    }
    res.json({ reply: output.trim() }); // ✅ 这里发送回前端
  });
});

// ======================== Mausoleums 接口 ========================
app.get('/api/mausoleums', (req, res) => {
  const filters = {
    dynasty: req.query.dynasty || '',
    province: req.query.province || '',
    city: req.query.city || ''
  };

  // 调用 Python 脚本
  const pythonProcess = spawn("python", [
    path.join(__dirname, "models", "mausoleums.py"),
    filters.dynasty,
    filters.province,
    filters.city
  ]);

  let output = "";

  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`Python error: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    if (code !== 0) {
      return res.status(500).json({ error: "Python script error" });
    }

    try {
      const jsonData = JSON.parse(output); // ✅ Python 输出 JSON
      res.json(jsonData);
    } catch (err) {
      console.error("解析 JSON 失败:", err);
      res.status(500).json({ error: "返回数据格式错误" });
    }
  });
});

app.use(express.static(path.join(__dirname, "../client/dist")));

app.get("/", (req, res) => {
  res.sendFile(path.join(__dirname, "../client/dist/index.html"));
});

app.listen(PORT, () => {
  console.log(`Backend started on http://localhost:${PORT}`);
});
