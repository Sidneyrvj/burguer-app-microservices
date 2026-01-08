@echo off
echo 🧪 Rodando testes do Product Service...
cd product-service && python -m pytest && cd ..

echo 🧪 Rodando testes do Auth Service...
cd auth-service && python -m pytest && cd ..

echo 🧪 Rodando testes do Order Service...
cd order-service && python -m pytest && cd ..

echo 🧪 Rodando testes do User Service...
cd user-service && python -m pytest && cd ..

echo ✅ Todos os testes concluídos!
pause
