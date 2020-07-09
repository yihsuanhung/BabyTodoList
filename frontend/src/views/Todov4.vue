<template>
  <div id="todov4">
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
    <br /><br />
    <table align="center">
      <td v-for="(item, index) in this.pagination.maxPage" :key="index">
        <button @click="apiIndex(item)">{{ item }}</button>
      </td>
    </table>
    <br /><br />
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
  name: "Todov4", //自己取的名字，最好跟檔名一樣
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
        }
        this.selection = [];
      }
    },
    async apiAdd(apiNewTask) {
      if (apiNewTask !== "") {
        this.pagination.page = 1
        let config = {
          baseURL: this.apiURL,
          url: "/add",
          method: "post",
          params: {
            page: this.pagination.page,
            limit: this.pagination.limit
          },
          data: JSON.stringify({ content: apiNewTask }),
        };
        let result = await sendReq(config);
        let data = result['data']
        this.calssifyTasks(data);
        this.apiNewTask = "";
      }
    },
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
      }
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
