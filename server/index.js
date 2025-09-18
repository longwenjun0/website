import express from 'express';
import cors from 'cors';
import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = process.env.PORT || 5000;


// 开启 CORS
app.use(cors({
  origin: "https://website-client-xxod.onrender.com", // 允许的前端地址
  methods: ["GET", "POST", "PUT", "DELETE"],          // 允许的请求方式
  credentials: true                                   // 如果要带 cookie
}));

// app.use(cors());
app.use(express.json());

// 启动后初始化数据库
function runPythonOnStartup() {
  const scriptPath = path.join(__dirname, "models", "init_db.py");
  const pythonCmd = process.env.PYTHON || "python3"; // 优先用 PYTHON 环境变量

  const pythonProcess = spawn(pythonCmd, [scriptPath]);

  let output = "";
  let errors = "";

  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    errors += data.toString();
  });

  pythonProcess.on("close", (code) => {
    if (code === 0) {
      console.log("✅ Python script executed successfully!");
      console.log(output);
    } else {
      console.error(`❌ Python script exited with code ${code}`);
      console.error("Error:", errors);
    }
  });
}

// 执行 Python
runPythonOnStartup();

app.use(express.static(path.join(__dirname, "../client/dist")));

app.get("/api/chat", (req, res) => {
  const model = req.query.model || "gpt-4o"; // 默认 gpt-4o
  const text = req.query.text;

  if (!text) {
    return res.status(400).json({ error: "No input text provided" });
  }

  console.log("received parameters", model, text);

  const pythonProcess = spawn("python3", [
    path.join(__dirname, "models", "run_model.py"),
    model,
    text,
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
    res.json({ reply: output.trim() });
  });
});

// ======================== Mausoleums 接口 ========================
app.get('/api/mausoleums', (req, res) => {
  const filters = {
    dynasty: req.query.dynasty || '',
    province: req.query.province || '',
    city: req.query.city || ''
  };

  console.log("received parameters", filters.dynasty, filters.province, filters.city);

  // 调用 Python 脚本
  const pythonProcess = spawn("python3", [
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
      console.error("json error:", err);
      res.status(500).json({ error: "Returned data format is wrong." });
    }
  });
});

// app.get("/", (req, res) => {
//   res.sendFile(path.join(__dirname, "../client/dist/index.html"));
// });

app.listen(PORT, () => {
  console.log(`Backend started on http://localhost:${PORT}`);
});
