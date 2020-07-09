<template>
  <div>
    <button @click="taskundo()">Undo</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
export default {
  name: "Undo",
  props: ["inArr", "inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port
    };
  },
  methods: {
    async taskundo() {
      if (this.inArr.length !== 0) {
        for (let i = 0; i < this.inArr.length; i++) {
          let taskId = this.inArr[i];
          let config = {
            baseURL: this.apiURL,
            url: "/undo/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("TasksOutUndo", data);
        }
        this.$forceUpdate();
      }
    }
  }
};
</script>
