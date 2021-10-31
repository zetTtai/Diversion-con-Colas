namespace Visitantes
{
    partial class Form1
    {
        /// <summary>
        /// Variable del diseñador necesaria.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Limpiar los recursos que se estén usando.
        /// </summary>
        /// <param name="disposing">true si los recursos administrados se deben desechar; false en caso contrario.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Código generado por el Diseñador de Windows Forms

        /// <summary>
        /// Método necesario para admitir el Diseñador. No se puede modificar
        /// el contenido de este método con el editor de código.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.label2 = new System.Windows.Forms.Label();
            this.IPValue = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.PortValue = new System.Windows.Forms.NumericUpDown();
            this.Mapa = new System.Windows.Forms.Panel();
            this.Conectar = new System.Windows.Forms.Button();
            this.Desconectar = new System.Windows.Forms.Button();
            this.Temporizador = new System.Windows.Forms.Timer(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.PortValue)).BeginInit();
            this.SuspendLayout();
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label2.Location = new System.Drawing.Point(26, 36);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(230, 24);
            this.label2.TabIndex = 3;
            this.label2.Text = "IP del servidor de Kafka";
            // 
            // IPValue
            // 
            this.IPValue.Location = new System.Drawing.Point(30, 77);
            this.IPValue.Name = "IPValue";
            this.IPValue.Size = new System.Drawing.Size(226, 20);
            this.IPValue.TabIndex = 4;
            this.IPValue.Text = "127.0.0.1";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label3.Location = new System.Drawing.Point(26, 124);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(157, 24);
            this.label3.TabIndex = 5;
            this.label3.Text = "Puerto de Kafka";
            // 
            // PortValue
            // 
            this.PortValue.Location = new System.Drawing.Point(30, 169);
            this.PortValue.Maximum = new decimal(new int[] {
            65555,
            0,
            0,
            0});
            this.PortValue.Name = "PortValue";
            this.PortValue.Size = new System.Drawing.Size(226, 20);
            this.PortValue.TabIndex = 6;
            this.PortValue.Value = new decimal(new int[] {
            9092,
            0,
            0,
            0});
            // 
            // Mapa
            // 
            this.Mapa.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(28)))), ((int)(((byte)(31)))), ((int)(((byte)(35)))));
            this.Mapa.Location = new System.Drawing.Point(276, 36);
            this.Mapa.Name = "Mapa";
            this.Mapa.Size = new System.Drawing.Size(500, 500);
            this.Mapa.TabIndex = 7;
            // 
            // Conectar
            // 
            this.Conectar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(10)))), ((int)(((byte)(10)))), ((int)(((byte)(12)))));
            this.Conectar.FlatAppearance.BorderSize = 0;
            this.Conectar.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Conectar.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.Conectar.Location = new System.Drawing.Point(30, 230);
            this.Conectar.Name = "Conectar";
            this.Conectar.Size = new System.Drawing.Size(226, 35);
            this.Conectar.TabIndex = 8;
            this.Conectar.Text = "Registrarse";
            this.Conectar.UseVisualStyleBackColor = false;
            this.Conectar.Click += new System.EventHandler(this.Conectar_Click);
            // 
            // Desconectar
            // 
            this.Desconectar.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(10)))), ((int)(((byte)(10)))), ((int)(((byte)(12)))));
            this.Desconectar.FlatAppearance.BorderSize = 0;
            this.Desconectar.Font = new System.Drawing.Font("Microsoft Sans Serif", 14.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Desconectar.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.Desconectar.Location = new System.Drawing.Point(30, 285);
            this.Desconectar.Name = "Desconectar";
            this.Desconectar.Size = new System.Drawing.Size(226, 35);
            this.Desconectar.TabIndex = 9;
            this.Desconectar.Text = "Salir";
            this.Desconectar.UseVisualStyleBackColor = false;
            this.Desconectar.Click += new System.EventHandler(this.Desconectar_Click);
            // 
            // Temporizador
            // 
            this.Temporizador.Interval = 3;
            this.Temporizador.Tick += new System.EventHandler(this.Temporizador_Tick);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(23)))), ((int)(((byte)(26)))), ((int)(((byte)(30)))));
            this.ClientSize = new System.Drawing.Size(799, 558);
            this.Controls.Add(this.Desconectar);
            this.Controls.Add(this.Conectar);
            this.Controls.Add(this.Mapa);
            this.Controls.Add(this.PortValue);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.IPValue);
            this.Controls.Add(this.label2);
            this.Name = "Form1";
            this.Text = "Visitante";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.PortValue)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox IPValue;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown PortValue;
        private System.Windows.Forms.Panel Mapa;
        private System.Windows.Forms.Button Conectar;
        private System.Windows.Forms.Button Desconectar;
        private System.Windows.Forms.Timer Temporizador;
    }
}