<template>
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title fs-5" id="exampleModalLabel">Добавление видео</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Закрыть"></button>
                </div>
                <div class="modal-body">
                    <div class="input-group mb-3">
                        <span class="input-group-text" id="basic-addon1">Название видео</span>
                        <input type="text" class="form-control" placeholder="Title" ref="title" aria-label="title"
                            v-on:change="handleTitleEdit()" aria-describedby="basic-addon1">
                    </div>
                    <div class="mb-3">
                        <input class="form-control" type="file" id="file" ref="file" v-on:change="handleFileUpload()"
                            accept=".mp4">
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Закрыть</button>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal"
                        @click="sendNewItem()">Добавить</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from "axios"

export default {
    name: 'AddItemModal',
    data() {
        return {
            host: "http://195.239.123.50:9000/",
            item: ""
        }
    },
    props: {
        id: String,
    },
    methods: {
        handleFileUpload() {
            this.file = this.$refs.file.files[0];
            console.log(this.file)
            console.log(this.title)
        },
        handleTitleEdit() {
            this.title = this.$refs.title.value
        },
        sendNewItem() {
            let formData = new FormData();
            formData.append('file', this.file);
            formData.append('title', this.title);
            this.$emit('start-add')
            axios.post('http://195.239.123.50:9000/items/add',
                formData,
                {
                    headers: {
                        'Content-Type': 'multipart/form-data'
                    }
                }
            ).then((resp) => {
                console.log(this);
                console.log(resp)
                this.$emit('add-event')
            })
                .catch(function (er) {
                    console.log(er);
                });
        }
    }
}
</script>