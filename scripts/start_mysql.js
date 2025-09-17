const { exec } = require('child_process');

// WSL 下启动 MySQL 服务
const cmd = 'sudo service mysql start';

exec(cmd, (err, stdout, stderr) => {
  if (err) {
    console.error('启动 MySQL 失败:', err);
    return;
  }
  console.log('MySQL 启动成功：\n', stdout);
  if (stderr) console.error('警告/错误输出：\n', stderr);
});
