<template>
  <div id="todo">
    <h3>TDL</h3>
    <Add
      :intest="inTest"
      :data="this.fetchedData"
      @outData="returnData($event)"
      @outPage="returnPage($event)"
    />

    <Tasks
      :inData="this.fetchedData"
      :inSelection="this.selection"
      :inPage="this.pagination.page"
      :inLimit="this.pagination.limit"
      @TasksOutEdit="returnData($event)"
      @TaskOutSelect="updateSelection($event)"
    />

    <Done
      :inArr="selection"
      :inPage="this.pagination.page"
      :inLimit="this.pagination.limit"
      @TasksOutDone="returnData($event)"
    />

    <Undo
      :inArr="selection"
      :inPage="this.pagination.page"
      :inLimit="this.pagination.limit"
      @TasksOutUndo="returnData($event)"
    />

    <Delete
      :inArr="selection"
      :inPage="this.pagination.page"
      :inLimit="this.pagination.limit"
      @TasksOutDelete="returnData($event)"
      @SelectionOut="updateSelection($event)"
    />

    <Pagination
      :page="this.pagination.page"
      :limit="this.pagination.limit"
      :dbLen="this.pagination.dbLen"
      :maxPage="this.pagination.maxPage"
      @PagesOut="returnPage($event)"
      @TaskOutIndex="returnData($event)"
    />

    <span v-show="selection.length !== 0">Selection: {{ selection }}</span>
  </div>
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";
import Add from "@/components/Add.vue";
import Tasks from "@/components/tasks.vue";
import Done from "@/components/Done.vue";
import Undo from "@/components/Undo.vue";
import Delete from "@/components/Delete.vue";
import Pagination from "@/components/Pagination.vue";
// import dTasks from "@/components/dtasks.vue";
import sendReq from "@/plugins/sendReq";
// import process from "@/plugins/sendReq";
// import classify from "@/plugins/classifier";
import { API } from "@/constants/config";
/* eslint-disable */
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue"; //把html引用進來
export default {
  //暴露出來讓Vue.app可以吃到
  name: "Todo", //自己取的名字，最好跟檔名一樣
  data() {
    return {
      inTest: "send in!",
      selection: [],
      selectStat: false,
      fetchedData: {
        undo: [],
        done: [],
      },
      apiNewTask: "",
      apiURL: API.Host + ":" + API.Port,
      apiConfig: {},
      pagination: {
        page: 1, 
        limit: 5
      },
    };
  },
  created() {
    this.getRequest();
  },
  methods: {
    async getRequest() {
      let config = {
        baseURL: this.apiURL,
        url: "/index",
        method: "get",
        params: this.pagination
      }
      let result = await sendReq(config); 
      let data = result['data']
      data = this.preprocess(data)
      this.calssifyTasks(data)
      // this.fetchedData.undo=[]
      // this.fetchedData.done=[]
      // classify(data, this.fetchedData.undo, this.fetchedData.done)

      //page
      this.pagination.dbLen = result['db_len']
      this.pagination.maxPage = Math.ceil(this.pagination.dbLen/this.pagination.limit)
    },
    preprocess(objArr){
      // Add two field, 'editStatus' and 'editContent', to each object
      let processed=[]
      for (let i = 0; i < objArr.length; i++){
        let obj = objArr[i]
        obj['editStatus'] = false;
        obj['editContent'] = '';
        processed.push(obj)
      }
      return processed
    },
    calssifyTasks(objArr) {
      // classify object array to 'done' or 'undo'
      this.fetchedData.undo = [];
      this.fetchedData.done = [];
      for (let i = 0; i < objArr.length; i++) {
        let data = objArr[i];
        if (data["status"] === 0) {
          this.fetchedData.undo.push(data);
        } else if (data["status"] === 1) {
          this.fetchedData.done.push(data);
        }
      }
      this.$forceUpdate();  
    },
    async apiIndex(page){
      let config = {
        baseURL: this.apiURL,
        url: "/index",
        method: "get",
        params: {
          page: page,
          limit: this.pagination.limit
        }
      }
      this.pagination.page = page
      let result = await sendReq(config);
      let data = result['data']
      this.calssifyTasks(data)
      // this.fetchedData.undo=[]
      // this.fetchedData.done=[]
      // classify(data, this.fetchedData.undo, this.fetchedData.done)
    },
    async apiDone() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/done/" + Number(taskId),
            method: "put",
            params: {
              page: this.pagination.page,
              limit: this.pagination.limit
            }
          }
          let result = await sendReq(config);
          let data = result['data']
          this.calssifyTasks(data);
          // this.fetchedData.undo=[]
          // this.fetchedData.done=[]
          // classify(data, this.fetchedData.undo, this.fetchedData.done)
        }
        this.selection = [];
      }
    },
    async apiUndo() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/undo/" + Number(taskId),
            method: "put",
            params: {
              page: this.pagination.page,
              limit: this.pagination.limit
            }
          };
          let result = await sendReq(config);
          let data = result['data']
          this.calssifyTasks(data);
          // this.fetchedData.undo=[]
          // this.fetchedData.done=[]
          // classify(data, this.fetchedData.undo, this.fetchedData.done)
        }
        this.selection = [];
      }
    },
    // async apiAdd(apiNewTask) {
    //   if (apiNewTask !== "") {
    //     this.pagination.page = 1
    //     let config = {
    //       baseURL: this.apiURL,
    //       url: "/add",
    //       method: "post",
    //       params: {
    //         page: this.pagination.page,
    //         limit: this.pagination.limit
    //       },
    //       data: JSON.stringify({ content: apiNewTask }),
    //     };
    //     let result = await sendReq(config);
    //     let data = result['data']
    //     // this.fetchedData.undo=[]
    //     // this.fetchedData.done=[]
    //     // classify(data, this.fetchedData.undo, this.fetchedData.done)
    //     this.calssifyTasks(data);
    //     this.apiNewTask = "";
    //   }
    // },
    async apiDelete() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = {
            baseURL: this.apiURL,
            url: "/delete/" + Number(taskId),
            method: "delete",
            params: {
              page: this.pagination.page,
              limit: this.pagination.limit
            }
          };
          let result = await sendReq(config);
          let data = result['data']
          this.calssifyTasks(data);
          // this.fetchedData.undo=[]
          // this.fetchedData.done=[]
          // classify(data, this.fetchedData.undo, this.fetchedData.done)
        }
      }
      this.selection = [];
    },
    apiEditStatSwitch(task_id, mode) {
      if (mode === "undo") {
        for (let i = 0; i < this.fetchedData.undo.length; i++) {
        if (this.fetchedData.undo[i]["id"] === task_id) {
          this.fetchedData.undo[i]["editStatus"] = !this.fetchedData.undo[i]["editStatus"]
          }
        }
      } else if (mode === "done") {
        for (let i = 0; i < this.fetchedData.done.length; i++) {
        if (this.fetchedData.done[i]["id"] === task_id) {
          this.fetchedData.done[i]["editStatus"] = !this.fetchedData.done[i]["editStatus"]
          }
        }
      }
      this.$forceUpdate();
    },
    async apiEdit(task_id, editedTask) {
      if (editedTask !== "") {
        let config = {
          baseURL: this.apiURL,
          url: "/edit/" + Number(task_id),
          method: "put",
          params: {
            page: this.pagination.page,
            limit: this.pagination.limit
          },
          data: JSON.stringify({ content: editedTask }),
        };
        let result = await sendReq(config);
        let data = result['data']
        this.calssifyTasks(data);
        // this.fetchedData.undo=[]
        // this.fetchedData.done=[]
        // classify(data, this.fetchedData.undo, this.fetchedData.done)
      }
    },
    // Component Functions
    returnData(data){
      data = this.preprocess(data)
      this.calssifyTasks(data)
    },
    updateSelection(arr){
      console.log('------', arr , '---------')
      this.selection = arr
    },
    returnSelection(arr, mode){
      if (mode === "delete") {
        this.selection = arr
      }else{
        for (let i = 0; i < arr.length; i++) {
          let task = arr[i];
          if (!this.selection.includes(task)) {
            this.selection.push(task);
          }
        }
        for (let i = 0; i < this.selection.length; i++) {
          let task = this.selection[i];
          if (!arr.includes(task)) {
            this.selection.splice(i, 1);
          }
        }
      }
    },
    returnPage(arr){
      this.pagination.page=arr.page
      this.pagination.limit=arr.limit
    },
    selectAll(arr, selection = this.selection) {
      for (let i = 0; i < arr.length; i++) {
        let task = arr[i]["id"];
        if (!selection.includes(task)) {
          selection.push(task);
        }
      }
    },
    // Selection Functions
    clearSelection(arr, selection = this.selection) {
      for (let i = 0; i < arr.length; i++) {
        let task = arr[i]["id"];
        if (selection.includes(task)) {
          selection.splice(selection.indexOf(task), 1);
        }
      }
    },
    reverseSelection(arr, selection = this.selection) {
      let allTasks = [];
      for (let i = 0; i < arr.length; i++) {
        let task = arr[i]["id"];
        if (selection.includes(task)) {
          selection.splice(selection.indexOf(task), 1);
        } else {
          selection.push(task);
        }
      }
    },
    selectAllFunction(mode) {
      if (mode === "undo"){
        this.selectAll(this.fetchedData.undo);
      } else if (mode === "done"){
        this.selectAll(this.fetchedData.done);
      } else if (mode === "all"){
        this.selectAll(this.fetchedData.undo.concat(this.fetchedData.done))
      }
    },
    clearFunction(mode) {
      if (mode === "undo"){
        this.clearSelection(this.fetchedData.undo);
      } else if (mode === "done"){
        this.clearSelection(this.fetchedData.done);
      } else if (mode === "all"){
        this.clearSelection(this.fetchedData.undo.concat(this.fetchedData.done))
      }
    },
    reverseFunction(mode) {
      if (mode === "undo"){
        this.reverseSelection(this.fetchedData.undo);
      } else if (mode === "done"){
        this.reverseSelection(this.fetchedData.done);
      } else if (mode === "all"){
        this.reverseSelection(this.fetchedData.undo.concat(this.fetchedData.done))
      }
    },
  },
  components: {
   HelloWorld,
   Add,
   Tasks,
   Done,
   Undo,
   Delete,
   Pagination
  }
};
</script>
<style lang="stylus">
.undoTasks {
    text-align:left;
    display: inline-block;
    list-style-type: none;
}
.doneTasks {
    color: #BDBDBD;
    text-align:left;
    display: inline-block;
    list-style-type: none;
}
.doneEditBut{
    color: #757575;
}

</style>
