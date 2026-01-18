Page({
  data: {
    // 使用本机 IP 地址，确保手机和模拟器都能访问
    url: 'http://192.168.3.29:8000/output_jiangmen/leaflet.html'
  },
  onLoad: function (options) {
    console.log("Map loading from: " + this.data.url);
  }
})