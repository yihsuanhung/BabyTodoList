import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    fakeInfo: {
      isLogin: false
    },
    vxSelection: [],
    vxFetchedData: {
      undo: [],
      done: []
    }
  },
  actions: {
    fakeCheckLoginStatus(commit, item) {
      // 要幹啥先做(call api或做資料前處理)
      console.log(item);
      commit.commit("fakeChange", true);
    },
    selectionAction(commit, selectionArr) {
      // console.log(selectionArr);
      commit.commit("updateSelection", selectionArr);
    },
    fetchedDataAction(commit, dataObj) {
      commit.commit("updateFetchedData", dataObj);
    }
  },
  mutations: {
    fakeChange(state, info) {
      // 寫檢查
      state.fakeInfo.isLogin = info;
    },
    updateSelection(state, selectionArr) {
      // console.log(selectionArr);
      state.vxSelection = selectionArr;
    },
    updateFetchedData(state, dataObj) {
      state.vxFetchedData = dataObj;
    }
  },
  modules: {}
});
