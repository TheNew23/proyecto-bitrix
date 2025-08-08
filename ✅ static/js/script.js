async function enviarMensaje() {
  const input = document.getElementById("input");
  const chatBox = document.getElementById("chat-box");
  const mensaje = input.value;

  if (!mensaje.trim()) return;

  chatBox.innerHTML += `<p><strong>Tú:</strong> ${mensaje}</p>`;
  input.value = "";

  const respuesta = await fetch("/webhook", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message: mensaje })
  });

  const data = await respuesta.json();
  chatBox.innerHTML += `<p><strong>IA:</strong> ${data.respuesta}</p>`;
  chatBox.scrollTop = chatBox.scrollHeight;
}
