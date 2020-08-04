import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    info: {
      isLogin: false
    }
  },
  actions: {
    checkLoginStatus(commit,item){
      // 要幹啥先做(call ＡＰＩ或做資料前處理)
      console.log(item)
      commit.commit('change',true)
    },
  },
  mutations: {
    change(state, info){
      // 寫檢查
      state.info.isLogin = info
    }
  },
  modules: {}
});
