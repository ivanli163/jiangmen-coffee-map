Page({
  data: {
    latitude: 0,
    longitude: 0,
    name: '',
    address: '',
    opened: false
  },

  onLoad: function (options) {
    if (options.lat && options.lng) {
      this.setData({
        latitude: parseFloat(options.lat),
        longitude: parseFloat(options.lng),
        name: decodeURIComponent(options.name || ''),
        address: decodeURIComponent(options.address || '')
      });
      this.openMap();
    }
  },

  openMap: function () {
    const that = this;
    wx.openLocation({
      latitude: that.data.latitude,
      longitude: that.data.longitude,
      name: that.data.name,
      address: that.data.address,
      scale: 18,
      success: function () {
        // 标记为已打开。当用户从地图返回时，onShow 会触发并执行返回逻辑
        that.setData({ opened: true });
      },
      fail: function(err) {
        console.error("Open Location Failed", err);
        wx.showToast({
          title: '打开地图失败',
          icon: 'none'
        });
      }
    });
  },

  onShow: function () {
    // 如果已经打开过地图（意味着现在是从地图界面返回的），则自动返回上一页
    if (this.data.opened) {
      wx.navigateBack();
    }
  },
  
  goBack: function() {
    wx.navigateBack();
  },
  
  reOpen: function() {
    this.openMap();
  }
})
