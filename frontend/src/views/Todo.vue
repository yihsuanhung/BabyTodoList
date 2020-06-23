<template>
  <div id="todo">
    <!-- 後端資料 -->
    <h3>TDL</h3>
    <pre>
      <input 
        type="text" 
        placeholder="Add new task"
        v-model="apiNewTask" 
        @keyup.enter="apiAdd(apiNewTask)"
      /> <button @click="apiAdd(apiNewTask)">Add</button>
    </pre>
    <!-- <button @click="getRequest()">Reload</button> |  -->
    <button @click="selectAllFunction('all')">Select All</button> |
    <button @click="reverseFunction('all')">Reverse</button> |
    <button @click="clearFunction('all')">Clear</button>

    <br /><br />
    <button @click="apiDone()">Done</button> |
    <button @click="apiUndo()">Undo</button> |
    <button @click="apiDelete()">Delete</button>

    <br /><br />
    <h4>Tasks todo</h4>
    <button @click="selectAllFunction('undo')">Select All</button> |
    <button @click="reverseFunction('undo')">Reverse</button> |
    <button @click="clearFunction('undo')">Clear</button>
    <br />
    <ul class="undoTasks">
      <li v-for="(item, index) in this.fetchedData.undo" :key="index">
        <input type="checkbox" :value="item['id']" v-model="selection" />
        {{ item["id"] }},
        {{ item["content"] }}
        <button
          @click="apiEditStatSwitch(item['id'], 'undo')"
          v-if="!item['editStatus']"
        >
          Edit
        </button>
        <input
          type="text"
          v-if="item['editStatus']"
          v-model="item['editContent']"
          @keyup.enter="apiEdit(item['id'], item['editContent'])"
        />
        <button
          @click="apiEdit(item['id'], item['editContent'])"
          v-if="item['editStatus']"
        >
          Update
        </button>
        <button
          @click="apiEditStatSwitch(item['id'], 'undo')"
          v-if="item['editStatus']"
        >
          Cancel
        </button>
      </li>
    </ul>

    <h4>Tasks done</h4>
    <button @click="selectAllFunction('done')">Select All</button> |
    <button @click="reverseFunction('done')">Reverse</button> |
    <button @click="clearFunction('done')">Clear</button>
    <br />
    <ul class="doneTasks">
      <li v-for="(item, index) in this.fetchedData.done" :key="index">
        <input type="checkbox" :value="item['id']" v-model="selection" />
        {{ item["id"] }},
        {{ item["content"] }}
        <button
          class="doneEditBut"
          @click="apiEditStatSwitch(item['id'], 'done')"
          v-if="!item['editStatus']"
        >
          Edit
        </button>
        <input
          type="text"
          v-if="item['editStatus']"
          v-model="item['editContent']"
          @keyup.enter="apiEdit(item['id'], item['editContent'])"
        />
        <button
          @click="apiEdit(item['id'], item['editContent'])"
          v-if="item['editStatus']"
        >
          Update
        </button>
        <button
          @click="apiEditStatSwitch(item['id'], 'done')"
          v-if="item['editStatus']"
        >
          Cancel
        </button>
      </li>
    </ul>

    <br /><br />
    <button @click="apiDone()">Done</button> |
    <button @click="apiUndo()">Undo</button> |
    <button @click="apiDelete()">Delete</button>
    <br /><br /><br />
    <span v-show="selection.length !== 0">Selection: {{ selection }}</span>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
/* eslint-disable */
// @ is an alias to /src
// import HelloWorld from "@/components/HelloWorld.vue"; //把html引用進來
export default {
  //暴露出來讓Vue.app可以吃到
  name: "Todo", //自己取的名字，最好跟檔名一樣
  data() {
    return {
      selection: [],
      selectStat: false,
      fetchedData: {
        undo: [],
        done: [],
      },
      apiNewTask: "",
      apiURL: API.Host + ":" + API.Port,
      apiConfig: {},
    };
  },
  created() {
    this.getRequest();
  },
  methods: {
    async getRequest() {
      let config = {
        baseURL: this.apiURL,
        url: "",
        method: "get"
      }
      let result = await sendReq(config); 
      // console.log("---before process---")
      // console.log(result)
      result = this.preprocess(result)
      // console.log("---after process---")
      // console.log(result)
      this.calssifyTasks(result)
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
      // console.log(this.fetchedData.undo)
      // console.log(this.fetchedData.done)
    },
    selectAll(arr, selection = this.selection) {
      for (let i = 0; i < arr.length; i++) {
        let task = arr[i]["id"];
        if (!selection.includes(task)) {
          selection.push(task);
        }
      }
    },
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
    async apiDone() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = this.apiConfig;
          config.url = "/done/" + Number(taskId);
          config.baseURL = this.apiURL;
          config.method = "put";
          let result = await sendReq(config);
          this.calssifyTasks(result);
        }
        this.selection = [];
      }
    },
    async apiUndo() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = this.apiConfig;
          config.url = "/undo/" + Number(taskId);
          config.baseURL = this.apiURL;
          config.method = "put";
          let result = await sendReq(config);
          this.calssifyTasks(result);
        }
        this.selection = [];
      }
    },
    async apiAdd(apiNewTask) {
      if (apiNewTask !== "") {
        let config = this.apiConfig;
        config.url = "/add";
        config.baseURL = this.apiURL;
        config.method = "post";
        config.data = JSON.stringify({ content: apiNewTask });
        let result = await sendReq(config);
        this.calssifyTasks(result);
        this.apiNewTask = "";
      }
    },
    async apiDelete() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
          let config = this.apiConfig;
          config.url = "/delete/" + Number(taskId);
          config.baseURL = this.apiURL;
          config.method = "delete";
          let result = await sendReq(config);
          this.calssifyTasks(result);
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
        let config = this.apiConfig;
        config.url = "/edit/" + Number(task_id);
        config.baseURL = this.apiURL;
        config.method = "put";
        config.data = JSON.stringify({ content: editedTask });
        let result = await sendReq(config);
        this.calssifyTasks(result);
        // this.fetchedData = result
      }
    },
  },
  //components: {
  //  HelloWorld //我要把他變成html標籤 <HelloWorld>
  //}
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
