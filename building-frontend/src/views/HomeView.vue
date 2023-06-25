<template>
  <nav class="navbar fixed-top navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
      <a class="navbar-brand" href="#">DDA</a>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup" aria-expanded="false">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
        </div>
      </div>
      <div class="d-flex mr-5">
        <button class="btn btn-success " type="button" data-bs-toggle="modal" data-bs-target="#exampleModal"
          :disabled="this.input_state">
          <div class="spinner-border spinner-border-sm text-light" role="status" v-if="this.input_state">
          </div><span v-if="!this.input_state"> +</span> Добавить
          видео
        </button>
      </div>
    </div>

  </nav>
  <div class="container">
    <div class="row mt-5">
      <div class="col-4 mt-5" v-for="item in items" :key="item">
        <ProcessingTemplate :id="item.id" :status="statuses[item.id]" @remove-event="getItems()" />
      </div>
    </div>
    <AddItemModal @add-event="finishAdd()" @start-add="this.input_state = true" />
  </div>
</template>

<script>
import ProcessingTemplate from "../components/ProcessingTemplate.vue"
import AddItemModal from "../components/AddItemModal.vue"
import axios from "axios"

export default {
  name: 'HomeView',
  components: {
    ProcessingTemplate,
    AddItemModal
  },
  data() {
    return {
      items: [],
      statuses: [],
      host: "http://195.239.123.50:9000/",
      input_state: false
    }
  },
  methods: {
    getItems() {
      axios.get(this.host + 'items/').then((resp) => {
        console.log(this);
        this.items = resp.data
      })
        .catch(function (er) {
          console.log(er);
        });
    },
    getStatuses() {
      axios.get(this.host + 'items/status').then((resp) => {
        console.log(this);
        this.statuses = resp.data
      })
        .catch(function (er) {
          console.log(er);
        });
    },
    finishAdd() {
      this.getItems()
      this.input_state = false
    },
    startAdd() {
      this.getItems()
      this.input_state = false
    }
  },
  created() {
    this.getItems()
    setInterval(() => {
      this.getStatuses()
    }, 5000);
  }
}
</script>
