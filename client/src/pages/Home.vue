<template>
  <div>
    <NavBar />
    <h2>帝王陵分布地图</h2>

    <!-- 筛选框 -->
    <div class="filters">
      <label>
        年代：
        <select v-model="filters.dynasty" @change="fetchData">
          <option value="all">All</option>
          <option v-for="d in dynasties" :key="d" :value="d">{{ d }}</option>
        </select>
      </label>

      <label>
        省份：
        <select v-model="filters.province" @change="fetchData">
          <option value="all">All</option>
          <option v-for="p in provinces" :key="p" :value="p">{{ p }}</option>
        </select>
      </label>

      <label>
        城市：
        <select v-model="filters.city" @change="fetchData">
          <option value="all">All</option>
          <option v-for="c in cities" :key="c" :value="c">{{ c }}</option>
        </select>
      </label>
    </div>

    <!-- 地图 -->
    <div id="map" style="height: 800px;"></div>
  </div>
</template>

<script setup>
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import { ref, reactive, onMounted, watch } from "vue";
import "leaflet/dist/leaflet.css";
import L from "leaflet";

// 响应式筛选条件
const filters = reactive({
  dynasty: "all",
  province: "all",
  city: "all"
});

// 朝代列表
const dynasties = ref([
  "夏","商","周","秦","西汉","东汉","三国","晋","南北朝","隋","唐","五代十国","宋","元","明","清","中华民国"
]);

// 中国省份 + 城市
const provincesWithCities = {
  "北京":["北京"],"天津":["天津"],"上海":["上海"],"重庆":["重庆"],
  "河北":["石家庄","唐山","保定","邯郸","廊坊","秦皇岛","沧州","承德","张家口","衡水","邢台"],
  "山西":["太原","大同","阳泉","长治","晋城","朔州","晋中","运城","忻州","临汾","吕梁"],
  "辽宁":["沈阳","大连","鞍山","抚顺","本溪","丹东","锦州","营口","阜新","辽阳","盘锦","铁岭","朝阳","葫芦岛"],
  "吉林":["长春","吉林","四平","辽源","通化","白山","松原","白城","延边"],
  "黑龙江":["哈尔滨","齐齐哈尔","牡丹江","佳木斯","大庆","鸡西","鹤岗","双鸭山","伊春","七台河","黑河","绥化","大兴安岭"],
  "江苏":["南京","无锡","徐州","常州","苏州","南通","连云港","淮安","盐城","扬州","镇江","泰州","宿迁"],
  "浙江":["杭州","宁波","温州","嘉兴","湖州","绍兴","金华","衢州","舟山","台州","丽水"],
  "安徽":["合肥","芜湖","蚌埠","淮南","马鞍山","淮北","铜陵","安庆","黄山","滁州","宿州","巢湖","六安","亳州","池州","宣城"],
  "福建":["福州","厦门","莆田","三明","泉州","漳州","南平","龙岩","宁德"],
  "江西":["南昌","景德镇","萍乡","九江","新余","鹰潭","赣州","吉安","宜春","抚州","上饶"],
  "山东":["济南","青岛","淄博","枣庄","东营","烟台","潍坊","济宁","泰安","威海","日照","临沂","德州","聊城","滨州","菏泽"],
  "河南":["郑州","开封","洛阳","平顶山","安阳","鹤壁","新乡","焦作","濮阳","许昌","漯河","三门峡","南阳","商丘","信阳","周口","驻马店","济源"],
  "湖北":["武汉","黄石","十堰","宜昌","襄阳","鄂州","荆门","孝感","荆州","黄冈","咸宁","随州","恩施","仙桃","潜江","天门","神农架"],
  "湖南":["长沙","株洲","湘潭","衡阳","邵阳","岳阳","常德","张家界","益阳","郴州","永州","怀化","娄底","湘西"],
  "广东":["广州","深圳","珠海","汕头","韶关","佛山","江门","湛江","茂名","肇庆","惠州","梅州","汕尾","河源","阳江","清远","东莞","中山","潮州","揭阳","云浮"],
  "广西":["南宁","柳州","桂林","梧州","北海","防城港","钦州","贵港","玉林","百色","贺州","河池","来宾","崇左"],
  "海南":["海口","三亚","三沙","儋州"],
  "四川":["成都","自贡","攀枝花","泸州","德阳","绵阳","广元","遂宁","内江","乐山","南充","眉山","宜宾","广安","达州","雅安","巴中","资阳","阿坝","甘孜","凉山"],
  "贵州":["贵阳","六盘水","遵义","安顺","毕节","铜仁","黔西南","黔东南","黔南"],
  "云南":["昆明","曲靖","玉溪","保山","昭通","丽江","普洱","临沧","楚雄","红河","文山","西双版纳","大理","德宏","怒江","迪庆"],
  "陕西":["西安","铜川","宝鸡","咸阳","渭南","延安","汉中","榆林","安康","商洛"],
  "甘肃":["兰州","嘉峪关","金昌","白银","天水","武威","张掖","平凉","酒泉","庆阳","定西","陇南","临夏","甘南"],
  "青海":["西宁","海东","海北","黄南","海南","果洛","玉树","海西"],
  "宁夏":["银川","石嘴山","吴忠","固原","中卫"],
  "新疆":["乌鲁木齐","克拉玛依","吐鲁番","哈密","昌吉","博尔塔拉","巴音郭楞","阿克苏","克孜勒苏","喀什","和田","伊犁","塔城","阿勒泰","石河子","阿拉尔","图木舒克","五家渠","北屯"],
  "香港":["香港"],
  "澳门":["澳门"],
  "台湾":["台北","高雄","台中","台南","新竹","嘉义","基隆","宜兰","桃园","苗栗","彰化","南投","云林","屏东","台东","花莲","澎湖"]
};


// 省份列表
const provinces = ref(Object.keys(provincesWithCities))

// 当前市列表
const cities = ref([])

// 监听省份变化，自动更新城市
watch(() => filters.province, (newProvince) => {
  if(newProvince && provincesWithCities[newProvince]){
    cities.value = provincesWithCities[newProvince]
  } else {
    cities.value = []
  }
  filters.city = ""
})

// Leaflet 地图和标记
let map = null
let markers = []

onMounted(() => {
  // 初始化地图
  map = L.map("map").setView([34.3416, 108.9398], 5)
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(map)

  // 标记北京为五角星
  const beijingIcon = L.divIcon({
    html: '★',   // 五角星字符
    className: 'star-marker', // 可自定义 CSS
    iconSize: [20, 20],
    iconAnchor: [10, 10]
  });

  L.marker([39.9042, 116.4074], { icon: beijingIcon })
    .addTo(map)
    .bindPopup("北京");

  // 加载其他数据点
  fetchData()
})


// 获取后端数据并更新地图
async function fetchData() {
  console.log("当前筛选条件:", JSON.stringify(filters));

  const queryParams = {};
  if (filters.dynasty) queryParams.dynasty = filters.dynasty;
  if (filters.province) queryParams.province = filters.province;
  if (filters.city) queryParams.city = filters.city;

  let mausoleums = []; // ⚠️ 提前声明

  try {
    const res = await axios.get('https://website-0lu7.onrender.com/api/mausoleums', { params: queryParams });
    mausoleums = res.data; // axios 自动解析 JSON
    console.log("返回数据:", mausoleums);
  } catch (error) {
    console.error("请求失败:", error);
    return; // 请求失败就不执行下面地图更新
  }

  // 清除旧标记
  markers.forEach(m => map.removeLayer(m));
  markers = [];

  // 添加新标记
  mausoleums.forEach(d => {
    if (d.lat && d.lng) {
      const marker = L.circleMarker([d.lat, d.lng], {
        radius: 6,
        color: "green",
        fillColor: "green",
        fillOpacity: 0.8
      }).addTo(map)
        .bindPopup(`
          <b>${d.tomb_name}</b><br>
          ${d.dynasty} ${d.emperor || ""} ${d.reign_title || ""} ${d.start_year || ""}-${d.end_year || ""}<br>
          ${d.province} ${d.city}
        `);
      markers.push(marker);
    }
  });
}

</script>

<style>
.filters{
  display:flex;
  gap:20px;
  padding:10px;
  background:#f9f9f9;
}
.filters label{
  display:flex;
  flex-direction:column;
}
.star-marker {
  font-size: 24px;
  color: red;
  text-shadow: 0 0 2px black;
}
</style>
