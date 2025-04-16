// pages/index.tsx

'use client';

import Navbar from "@/components/NavBar";
import React, { useState, useEffect } from "react";

const Home = () => {
  const [devices, setDevices] = useState<any[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);

  const devicesPerPage = 5;

  const fetchDevices = async (page: number) => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/api/v1/devices/?page=${page}&limit=${devicesPerPage}`);
      const data = await res.json();
      setDevices(data.devices);
      setTotalPages(Math.ceil(data.total / devicesPerPage));
    } catch (error) {
      console.error("Erro ao buscar dispositivos", error);
    }
  };

  useEffect(() => {
    fetchDevices(currentPage);
  }, [currentPage]);

  const handlePrevPage = () => {
    if (currentPage > 1) {
      setCurrentPage(currentPage - 1);
    }
  };

  const handleNextPage = () => {
    if (currentPage < totalPages) {
      setCurrentPage(currentPage + 1);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <main className="p-6">
        <section className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
          {/* Visão Geral da Rede */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Visão Geral</h2>
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 bg-green-100 rounded-lg">
                <h3 className="font-medium">Dispositivos Ativos</h3>
                <p>5</p>
              </div>
              <div className="p-4 bg-yellow-100 rounded-lg">
                <h3 className="font-medium">Alertas Pendentes</h3>
                <p>3</p>
              </div>
            </div>
          </div>

          {/* Ações Rápidas */}
          <div className="bg-white p-6 rounded-lg shadow-lg">
            <h2 className="text-xl font-semibold mb-4">Ações Rápidas</h2>
            <button className="w-full bg-blue-500 text-white p-3 rounded-lg hover:bg-blue-600">
              Configurar Dispositivos
            </button>
            <button className="w-full bg-gray-300 text-gray-700 p-3 mt-4 rounded-lg hover:bg-gray-400">
              Monitorar Rede
            </button>
          </div>
        </section>

        {/* Tabela de Dispositivos */}
        <section className="mt-8">
          <h2 className="text-2xl font-semibold mb-4">Dispositivos</h2>
          <table className="min-w-full bg-white border border-gray-300 rounded-lg shadow-md">
            <thead>
              <tr className="bg-gray-200">
                <th className="px-4 py-2 text-left">Hostname</th>
                <th className="px-4 py-2 text-left">Tipo</th>
                <th className="px-4 py-2 text-left">IP de Gerência</th>
                <th className="px-4 py-2 text-left">Ações</th>
              </tr>
            </thead>
            <tbody>
              {devices?.map((device: any) => (
                <tr key={device.id} className="hover:bg-gray-100">
                  <td className="px-4 py-2">{device.hostname}</td>
                  <td className="px-4 py-2">{device.device_type}</td>
                  <td className="px-4 py-2">{device.device_mgmt_ipv4}</td>
                  <td className="px-4 py-2">
                    <button className="bg-blue-500 text-white px-3 py-1 rounded hover:bg-blue-600">
                      Ver Detalhes
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {/* Paginação */}
          <div className="flex justify-between mt-6">
            <button
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
              onClick={handlePrevPage}
              disabled={currentPage === 1}
            >
              Anterior
            </button>
            <span className="self-center text-lg">
              Página {currentPage} de {totalPages}
            </span>
            <button
              className="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400"
              onClick={handleNextPage}
              disabled={currentPage === totalPages}
            >
              Próxima
            </button>
          </div>
        </section>
      </main>
    </div>
  );
};

export default Home;
