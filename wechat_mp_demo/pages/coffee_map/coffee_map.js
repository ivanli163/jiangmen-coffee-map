Page({
  data: {
    // 5.0 全链路集成版 - 咖啡地图
    url: 'http://192.168.3.29:8000/output_jiangmen/coffee_map.html'
  },
  onLoad: function (options) {
    console.log("Loading Coffee Map V5.0");
  },
  onShareAppMessage: function () {
    return {
      title: '江门咖啡地图 5.0',
      path: '/pages/coffee_map/coffee_map'
    }
  }
})
