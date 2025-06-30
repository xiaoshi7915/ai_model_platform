const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  // 转译依赖
  transpileDependencies: true,
  
  // 开发服务器配置
  devServer: {
    host: '0.0.0.0',  // 允许外部访问
    port: 5588,
    proxy: {
      '/api': {
        target: "http://localhost:5688",
        changeOrigin: true,
        ws: true,
        timeout: 30000, // 超时时间
        onError: (err, req, res) => {
          console.error('代理请求错误:', err);
          if (!res.headersSent) {
            res.writeHead(500, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: '服务器连接失败，请稍后重试' }));
          }
        },
        onProxyReq: (proxyReq, req, res) => {
          console.log('代理请求:', req.method, req.url);
        },
        onProxyRes: (proxyRes, req, res) => {
          console.log('代理响应:', proxyRes.statusCode, req.url);
        }
      }
    },
    client: {
      webSocketURL: 'auto://0.0.0.0:0/ws',
      overlay: {
        errors: true,
        warnings: false,
      }
    }
  },
  
  // 生产环境配置
  productionSourceMap: false,
  
  // 静态资源路径
  publicPath: '/',
  
  // 构建输出目录
  outputDir: 'dist',
  
  // 放置静态资源的目录
  assetsDir: 'static',
  
  // 检查并修复 vue.config.js 文件
  lintOnSave: process.env.NODE_ENV === 'development',
  
  // 提供 webpack 配置
  configureWebpack: {
    resolve: {
      alias: {
        '@': require('path').resolve(__dirname, 'src')
      }
    },
    // 性能提示
    performance: {
      hints: false
    }
  }
}) 