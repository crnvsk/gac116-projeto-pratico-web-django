<template>
  <div class="container">
    <h1 class="title">Gerenciamento de Usuários</h1>

    <div class="form-container">
      <button @click="toggleModal(true)" class="button centered-button">Criar Novo Usuário</button>
    </div>

    <!-- Tabela de Usuários -->
    <div>
      <h2 class="subtitle">Lista de Usuários</h2>
      <table class="item-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Usuário</th>
            <th>Ações</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>
              <button @click="toggleTicketModal(true, user)" class="button">Criar Ticket</button>
              <button @click="viewUserTickets(user)" class="button">Ver Tickets</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Modal para criar ticket -->
    <div v-if="showTicketModal" class="modal">
      <div class="modal-content">
        <h2>Criar Ticket para {{ selectedUser.username }}</h2>
        <input v-model="currentTicket.title" class="input" placeholder="Título do Ticket" />
        <textarea v-model="currentTicket.description" class="input" placeholder="Descrição do Ticket"></textarea>
        <button @click="createMockTicket" class="button register-button">Criar</button>
        <button @click="toggleTicketModal(false)" class="button cancel-button">Cancelar</button>
      </div>
    </div>

    <!-- Modal para visualizar e editar tickets -->
    <div v-if="showViewTicketsModal" class="modal">
      <div class="modal-content">
        <h2>Tickets de {{ selectedUser.username }}</h2>
        <div v-for="ticket in userTickets" :key="ticket.id" class="ticket-item">
          <p><strong>ID:</strong> {{ ticket.id }}</p>
          <p><strong>Título:</strong> {{ ticket.title }}</p>
          <p><strong>Descrição:</strong> {{ ticket.description }}</p>
          <button @click="editTicket(ticket)" class="button">Editar</button>
          <button @click="deleteTicket(ticket)" class="button cancel-button">Excluir</button>
        </div>
        <button @click="toggleViewTicketsModal(false)" class="button cancel-button">Fechar</button>
      </div>
    </div>

    <!-- Modal para criar usuário -->
    <div v-if="showModal" class="modal">
      <div class="modal-content">
        <h2>Cadastro de Usuário</h2>
        <input v-model="currentUser.username" class="input" placeholder="Usuário" />
        <input v-model="currentUser.password" class="input" type="password" placeholder="Senha" />
        <label for="role">Tipo de Usuário:</label>
        <select v-model="currentUser.role" id="role" class="input">
          <option value="client">Cliente</option>
          <option value="employee">Funcionário</option>
        </select>
        <button @click="registerUser" class="button register-button">Registrar</button>
        <button @click="toggleModal(false)" class="button cancel-button">Cancelar</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      users: [],
      tickets: [],
      userTickets: [],
      showModal: false,
      showTicketModal: false,
      showViewTicketsModal: false,
      selectedUser: null,
      currentUser: {
        username: '',
        password: '',
        role: 'client',
      },
      currentTicket: {
        title: '',
        description: '',
        status: 'Aberto',
      },
    };
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/users/');
        if (!response.ok) throw new Error('Erro ao buscar usuários');
        this.users = await response.json();
      } catch (error) {
        console.error('Erro ao buscar usuários:', error);
      }
    },
    async registerUser() {
      try {
        console.log('Enviando requisição:', this.currentUser);
        const response = await fetch('http://127.0.0.1:8000/api/register/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.currentUser.username,
            password: this.currentUser.password,
            role: this.currentUser.role
          })
        });
        if (!response.ok) throw new Error('Erro ao registrar usuário');
        const data = await response.json();
        alert('Usuário registrado com sucesso!');
        this.toggleModal(false);
        this.users.push({ id: data.user.id, username: data.user.username });
      } catch (error) {
        console.error('Erro ao registrar usuário:', error);
        alert(`Erro: ${error.message}`);
      }
    },
    toggleModal(isOpen) {
      this.showModal = isOpen;
      if (!isOpen) {
        this.resetForm();
      }
    },
    toggleTicketModal(isOpen, user = null) {
      this.showTicketModal = isOpen;
      this.selectedUser = user;
      if (!isOpen) {
        this.resetTicketForm();
      }
    },
    toggleViewTicketsModal(isOpen) {
      this.showViewTicketsModal = isOpen;
    },
    resetForm() {
      this.currentUser = {
        username: '',
        password: '',
        role: 'client',
      };
    },
    resetTicketForm() {
      this.currentTicket = {
        title: '',
        description: '',
        status: 'Aberto',
      };
    },
    createMockTicket() {
      if (!this.currentTicket.title || !this.currentTicket.description) {
        alert('Preencha todos os campos obrigatórios!');
        return;
      }
      const newTicket = {
        id: this.tickets.length + 1,
        title: this.currentTicket.title,
        description: this.currentTicket.description,
        status: 'Aberto',
        userId: this.selectedUser.id,
      };
      this.tickets.push(newTicket);
      alert(`Ticket criado com sucesso para o usuário ${this.selectedUser.username}!`);
      this.toggleTicketModal(false);
    },
    viewUserTickets(user) {
      this.userTickets = this.tickets.filter(ticket => ticket.userId === user.id);
      this.selectedUser = user;
      this.toggleViewTicketsModal(true);
    },
    editTicket(ticket) {
      const updatedTitle = prompt('Editar título do ticket:', ticket.title);
      const updatedDescription = prompt('Editar descrição do ticket:', ticket.description);
      if (updatedTitle !== null) ticket.title = updatedTitle;
      if (updatedDescription !== null) ticket.description = updatedDescription;
    },
    deleteTicket(ticket) {
      const confirmDelete = confirm('Deseja realmente excluir este ticket?');
      if (confirmDelete) {
        this.tickets = this.tickets.filter(t => t.id !== ticket.id);
        alert('Ticket excluído com sucesso!');
      }
    },
  },
  created() {
    this.fetchUsers();
  },
};
</script>

<style>
/* Reaproveitando os estilos do TicketManager.vue */
@import '../assets/styles/ItemManager.css';
</style>
