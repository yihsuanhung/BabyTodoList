<template>
  <div>
    <pre>
      <input 
        type="text" 
        placeholder="Add new task"
        v-model="newTask" 
        v-on:input="Text = $event" 
        @keyup.enter="Add(newTask)"
      /> <button @click="Add(newTask)">Add</button>
    </pre>
  </div>
</template>

<script>
import sendReq from "@/plugins/sendReq";
// import classify from "@/plugins/classifier";
import { API, Pagination } from "@/constants/config";
export default {
  name: "Add",
  props: [],
  data() {
    return {
      newTask: "",
      apiURL: API.Host + ":" + API.Port,
      pagination: {
        page: 1,
        limit: Pagination.limit
      }
    };
  },
  methods: {
    async Add(newTask) {
      if (newTask !== "") {
        let config = {
          baseURL: this.apiURL,
          url: "/add",
          method: "post",
          params: {
            page: this.pagination.page,
            limit: this.pagination.limit
          },
          data: JSON.stringify({ content: newTask })
        };
        let result = await sendReq(config);
        let data = result["data"];
        this.$emit("outData", data);
        this.$emit("outPage", {
          page: this.pagination.page,
          limit: this.pagination.limit
        });
        this.newTask = "";
      }
    }
  }
};
</script>
