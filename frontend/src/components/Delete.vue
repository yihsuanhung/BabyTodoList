<template>
  <div>
    <button @click="taskdelete()">Delete</button>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
import { API } from "@/constants/config";
import { EventBus } from "@/plugins/bus.js";
export default {
  name: "Delete",
  props: ["inPage", "inLimit"],
  data() {
    return {
      apiURL: API.Host + ":" + API.Port,
      selection: []
    };
  },
  methods: {
    async taskdelete() {
      if (this.selection.length !== 0) {
        for (let i = 0; i < this.selection.length; i++) {
          let taskId = this.selection[i];
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
          this.$emit("outData", data);
        }
        this.$forceUpdate();
        // this.$emit("SelectionOut", []);
        EventBus.$emit("TasksSelectionBus", []);
      }
    }
  },
  created() {
    EventBus.$on("TasksSelectionBus", arr => {
      this.selection = arr;
    });
  }
};
</script>
