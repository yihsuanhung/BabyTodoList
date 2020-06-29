<template>
  <div>
    <label>新增</label>
    <input v-model="newData" type="text" />
    <button @click="add">新增</button>

    <br /><br />
    <button @click="Done()">更改狀態：完成</button> |
    <button @click="Undo()">更改狀態：未完成</button> |
    <button @click="Delete()">刪除</button>

    <br /><br />
    <h4>未完成</h4>
    <ul>
      <li
        v-for="(item, index) in this.OriData"
        :key="index"
        v-show="item.status == 0"
      >
        <input type="checkbox" :value="item.id" v-model="select" />
        <label v-show="!item.editStatus">{{ item.content }}</label>
        <input v-show="item.editStatus" v-model="item.content" type="text" />
        <button @click="editor(index, true, item.content)">編輯</button>
        <button v-show="item.editStatus" @click="editor(index, false)">
          取消
        </button>
      </li>
    </ul>

    <br /><br />
    <h4>已完成</h4>
    <ul>
      <li
        v-for="(item, index) in this.OriData"
        :key="index"
        v-show="item.status == 1"
      >
        <input type="checkbox" :value="item.id" v-model="select" />
        <label v-show="!item.editStatus">{{ item.content }}</label>
        <input v-show="item.editStatus" :value="item.content" type="text" />
        <button @click="editor(index, true)">編輯</button>
        <button v-show="item.editStatus" @click="editor(index, false)">
          取消
        </button>
      </li>
    </ul>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";

export default {
  name: "Daniel",
  components: {},
  data() {
    return {
      newData: "",
      tmpEdit: "",
      OriData: [],
      url: API.Host + ":" + API.Port,
      select: [],
      submitStatus: false
    };
  },
  async created() {
    await this.getList();
  },
  methods: {
    async getList() {
      let config = {
        url: this.url,
        method: "get"
      };
      let result = await sendReq(config);
      this.OriData = this.conv(result);
    },
    async editor(index, uploadStatus, value = null) {
      if (uploadStatus && value !== null) {
        this.tmpEdit = value;
      }
      if (!uploadStatus) {
        this.OriData[index].content = this.tmpEdit;
        this.tmpEdit = "";
      }

      this.OriData[index].editStatus = !this.OriData[index].editStatus;
    },
    conv(result) {
      let returnData = [];
      for (let item in result) {
        let itemData = {};
        itemData["id"] = result[item]["id"];
        itemData["content"] = result[item]["content"];
        itemData["status"] = result[item]["status"];
        itemData["editStatus"] = false;
        itemData["editContent"] = "";
        returnData.push(itemData);
      }
      console.log(returnData);
      return returnData;
    },
    async add() {
      let config = {
        baseURL: this.url,
        url: "/add",
        method: "post",
        data: JSON.stringify({ content: this.newData })
      };
      let result = await sendReq(config);
      this.newData = "";
      this.OriData = this.conv(result);
    },
    async Done() {
      if (this.select.length !== 0) {
        for (let i in this.select) {
          let config = {
            baseURL: this.url,
            url: "/done/" + Number(this.select[i]),
            method: "put"
          };
          let result = await sendReq(config);
          this.OriData = this.conv(result);
        }
      }
      this.select = [];
    },
    async Undo() {
      if (this.select.length !== 0) {
        for (let i in this.select) {
          let config = {
            baseURL: this.url,
            url: "/undo/" + Number(this.select[i]),
            method: "put"
          };
          let result = await sendReq(config);
          this.OriData = this.conv(result);
        }
      }
      this.select = [];
    },
    async Delete() {
      if (this.select.length !== 0) {
        for (let i in this.select) {
          let config = {
            baseURL: this.url,
            url: "/delete/" + Number(this.select[i]),
            method: "delete",
            data: JSON.stringify({ content: this.newData })
          };
          await sendReq(config);
        }
      }
      this.select = [];
    }
  }
};
</script>
