<template>
  <div>
    <button @click="taskdelete()">Delete</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
export default {
  name: "Delete",
  props: ["inArr", "inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
    };
  },
  methods: {
    async taskdelete() {
      if (this.inArr.length !== 0) {
        for (let i = 0; i < this.inArr.length; i++) {
          let taskId = this.inArr[i];
          let config = {
            baseURL: this.apiURL,
            url: "/delete/" + Number(taskId),
            method: "delete",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("TasksOutDelete", data);
        }
        this.$forceUpdate();
        this.$emit("SelectionOut", []);
      }
    }
  }
};
</script>
