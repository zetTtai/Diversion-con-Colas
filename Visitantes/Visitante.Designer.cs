namespace Visitantes
{
    partial class Visitante
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
            this.IPValueKafka = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.PortValueKafka = new System.Windows.Forms.NumericUpDown();
            this.Mapa = new System.Windows.Forms.Panel();
            this.Conectar = new System.Windows.Forms.Button();
            this.Desconectar = new System.Windows.Forms.Button();
            this.Temporizador = new System.Windows.Forms.Timer(this.components);
            this.label1 = new System.Windows.Forms.Label();
            this.IPValueRegistry = new System.Windows.Forms.TextBox();
            this.label4 = new System.Windows.Forms.Label();
            this.PortValueRegistry = new System.Windows.Forms.NumericUpDown();
            this.panel1 = new System.Windows.Forms.Panel();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.label7 = new System.Windows.Forms.Label();
            this.ColorPicker = new System.Windows.Forms.ColorDialog();
            this.VisitorName = new System.Windows.Forms.TextBox();
            this.VisitorPassword = new System.Windows.Forms.TextBox();
            this.VisitorAlias = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.PortValueKafka)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.PortValueRegistry)).BeginInit();
            this.SuspendLayout();
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label2.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label2.Location = new System.Drawing.Point(12, 9);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(199, 20);
            this.label2.TabIndex = 3;
            this.label2.Text = "IP del servidor de Kafka";
            // 
            // IPValueKafka
            // 
            this.IPValueKafka.Location = new System.Drawing.Point(16, 36);
            this.IPValueKafka.Name = "IPValueKafka";
            this.IPValueKafka.Size = new System.Drawing.Size(195, 20);
            this.IPValueKafka.TabIndex = 4;
            this.IPValueKafka.Text = "127.0.0.1";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label3.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label3.Location = new System.Drawing.Point(12, 72);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(138, 20);
            this.label3.TabIndex = 5;
            this.label3.Text = "Puerto de Kafka";
            // 
            // PortValueKafka
            // 
            this.PortValueKafka.Location = new System.Drawing.Point(16, 99);
            this.PortValueKafka.Maximum = new decimal(new int[] {
            65555,
            0,
            0,
            0});
            this.PortValueKafka.Name = "PortValueKafka";
            this.PortValueKafka.Size = new System.Drawing.Size(195, 20);
            this.PortValueKafka.TabIndex = 6;
            this.PortValueKafka.Value = new decimal(new int[] {
            9092,
            0,
            0,
            0});
            // 
            // Mapa
            // 
            this.Mapa.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(28)))), ((int)(((byte)(31)))), ((int)(((byte)(35)))));
            this.Mapa.Location = new System.Drawing.Point(239, 12);
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
            this.Conectar.Location = new System.Drawing.Point(16, 436);
            this.Conectar.Name = "Conectar";
            this.Conectar.Size = new System.Drawing.Size(195, 35);
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
            this.Desconectar.Location = new System.Drawing.Point(16, 477);
            this.Desconectar.Name = "Desconectar";
            this.Desconectar.Size = new System.Drawing.Size(195, 35);
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
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label1.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label1.Location = new System.Drawing.Point(12, 136);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(122, 20);
            this.label1.TabIndex = 10;
            this.label1.Text = "IP de Registry";
            // 
            // IPValueRegistry
            // 
            this.IPValueRegistry.Location = new System.Drawing.Point(16, 163);
            this.IPValueRegistry.Name = "IPValueRegistry";
            this.IPValueRegistry.Size = new System.Drawing.Size(195, 20);
            this.IPValueRegistry.TabIndex = 11;
            this.IPValueRegistry.Text = "127.0.0.1";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label4.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label4.Location = new System.Drawing.Point(12, 197);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(158, 20);
            this.label4.TabIndex = 12;
            this.label4.Text = "Puerto de Registry";
            // 
            // PortValueRegistry
            // 
            this.PortValueRegistry.Location = new System.Drawing.Point(16, 224);
            this.PortValueRegistry.Maximum = new decimal(new int[] {
            65555,
            0,
            0,
            0});
            this.PortValueRegistry.Name = "PortValueRegistry";
            this.PortValueRegistry.Size = new System.Drawing.Size(195, 20);
            this.PortValueRegistry.TabIndex = 13;
            this.PortValueRegistry.Value = new decimal(new int[] {
            9092,
            0,
            0,
            0});
            // 
            // panel1
            // 
            this.panel1.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(28)))), ((int)(((byte)(31)))), ((int)(((byte)(35)))));
            this.panel1.Location = new System.Drawing.Point(763, 12);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(368, 500);
            this.panel1.TabIndex = 8;
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label5.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label5.Location = new System.Drawing.Point(12, 266);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(48, 20);
            this.label5.TabIndex = 14;
            this.label5.Text = "Alias";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label6.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label6.Location = new System.Drawing.Point(12, 318);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(71, 20);
            this.label6.TabIndex = 15;
            this.label6.Text = "Nombre";
            // 
            // label7
            // 
            this.label7.AutoSize = true;
            this.label7.Font = new System.Drawing.Font("Microsoft Sans Serif", 12F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.label7.ForeColor = System.Drawing.SystemColors.ButtonFace;
            this.label7.Location = new System.Drawing.Point(12, 371);
            this.label7.Name = "label7";
            this.label7.Size = new System.Drawing.Size(102, 20);
            this.label7.TabIndex = 16;
            this.label7.Text = "Contraseña";
            // 
            // VisitorName
            // 
            this.VisitorName.Location = new System.Drawing.Point(16, 341);
            this.VisitorName.Name = "VisitorName";
            this.VisitorName.Size = new System.Drawing.Size(195, 20);
            this.VisitorName.TabIndex = 17;
            // 
            // VisitorPassword
            // 
            this.VisitorPassword.Location = new System.Drawing.Point(16, 394);
            this.VisitorPassword.Name = "VisitorPassword";
            this.VisitorPassword.Size = new System.Drawing.Size(195, 20);
            this.VisitorPassword.TabIndex = 18;
            // 
            // VisitorAlias
            // 
            this.VisitorAlias.Location = new System.Drawing.Point(16, 289);
            this.VisitorAlias.Name = "VisitorAlias";
            this.VisitorAlias.Size = new System.Drawing.Size(195, 20);
            this.VisitorAlias.TabIndex = 19;
            this.VisitorAlias.Enter += new System.EventHandler(this.Alias_Enter);
            // 
            // Visitante
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(23)))), ((int)(((byte)(26)))), ((int)(((byte)(30)))));
            this.ClientSize = new System.Drawing.Size(1139, 523);
            this.Controls.Add(this.VisitorAlias);
            this.Controls.Add(this.VisitorPassword);
            this.Controls.Add(this.VisitorName);
            this.Controls.Add(this.label7);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.PortValueRegistry);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.IPValueRegistry);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.Desconectar);
            this.Controls.Add(this.Conectar);
            this.Controls.Add(this.Mapa);
            this.Controls.Add(this.PortValueKafka);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.IPValueKafka);
            this.Controls.Add(this.label2);
            this.Name = "Visitante";
            this.Text = " ";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.PortValueKafka)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.PortValueRegistry)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox IPValueKafka;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.NumericUpDown PortValueKafka;
        private System.Windows.Forms.Panel Mapa;
        private System.Windows.Forms.Button Conectar;
        private System.Windows.Forms.Button Desconectar;
        private System.Windows.Forms.Timer Temporizador;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox IPValueRegistry;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.NumericUpDown PortValueRegistry;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.Label label7;
        private System.Windows.Forms.ColorDialog ColorPicker;
        private System.Windows.Forms.TextBox VisitorName;
        private System.Windows.Forms.TextBox VisitorPassword;
        private System.Windows.Forms.TextBox VisitorAlias;
    }
}