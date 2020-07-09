<template>
  <div>
    <button @click="taskdone()">Done</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
export default {
  name: "Done",
  props: ["inArr", "inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port
    };
  },
  methods: {
    async taskdone() {
      if (this.inArr.length !== 0) {
        for (let i = 0; i < this.inArr.length; i++) {
          let taskId = this.inArr[i];
          let config = {
            baseURL: this.apiURL,
            url: "/done/" + Number(taskId),
            method: "put",
            params: {
              page: this.inPage,
              limit: this.inLimit
            }
          };
          let result = await sendReq(config);
          let data = result["data"];
          this.$emit("TasksOutDone", data);
          this.outData = data;
        }
        this.$forceUpdate();

        // this.$emit("SelectionOut", [])
      }
    }
  }
};
</script>
