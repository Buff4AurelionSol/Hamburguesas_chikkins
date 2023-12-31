PGDMP         7                {            Restaurant_Chikkins    15.3    15.3                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    24578    Restaurant_Chikkins    DATABASE     �   CREATE DATABASE "Restaurant_Chikkins" WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'Spanish_Spain.1252';
 %   DROP DATABASE "Restaurant_Chikkins";
             	   TonyJDL23    false                       0    0    DATABASE "Restaurant_Chikkins"    COMMENT     U   COMMENT ON DATABASE "Restaurant_Chikkins" IS 'Restaurante de hamburguesas CHIKKINS';
                	   TonyJDL23    false    3334            �            1259    24642    cliente    TABLE     �   CREATE TABLE public.cliente (
    cedula integer NOT NULL,
    nombre character varying(30),
    whatsapp character varying(13),
    email character varying(50)
);
    DROP TABLE public.cliente;
       public         heap    postgres    false            �            1259    33015    pedido    TABLE     �  CREATE TABLE public.pedido (
    num_pedido integer NOT NULL,
    cant_hambur integer,
    monto_delivery real,
    total_pagar real,
    modo_pago character varying(10),
    sreen_pago bytea,
    status character varying(12) DEFAULT 'pending'::character varying NOT NULL,
    fecha_hora character varying(22),
    ciudad character varying(15),
    municipio character varying(15),
    observacion text,
    ced_cliente integer NOT NULL
);
    DROP TABLE public.pedido;
       public         heap    postgres    false            �            1259    33014    pedido_num_pedido_seq    SEQUENCE     �   CREATE SEQUENCE public.pedido_num_pedido_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 ,   DROP SEQUENCE public.pedido_num_pedido_seq;
       public          postgres    false    216                       0    0    pedido_num_pedido_seq    SEQUENCE OWNED BY     O   ALTER SEQUENCE public.pedido_num_pedido_seq OWNED BY public.pedido.num_pedido;
          public          postgres    false    215            i           2604    33018    pedido num_pedido    DEFAULT     v   ALTER TABLE ONLY public.pedido ALTER COLUMN num_pedido SET DEFAULT nextval('public.pedido_num_pedido_seq'::regclass);
 @   ALTER TABLE public.pedido ALTER COLUMN num_pedido DROP DEFAULT;
       public          postgres    false    215    216    216            �          0    24642    cliente 
   TABLE DATA           B   COPY public.cliente (cedula, nombre, whatsapp, email) FROM stdin;
    public          postgres    false    214   S                  0    33015    pedido 
   TABLE DATA           �   COPY public.pedido (num_pedido, cant_hambur, monto_delivery, total_pagar, modo_pago, sreen_pago, status, fecha_hora, ciudad, municipio, observacion, ced_cliente) FROM stdin;
    public          postgres    false    216   �       	           0    0    pedido_num_pedido_seq    SEQUENCE SET     D   SELECT pg_catalog.setval('public.pedido_num_pedido_seq', 24, true);
          public          postgres    false    215            l           2606    24646    cliente cliente_pkey 
   CONSTRAINT     V   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (cedula);
 >   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_pkey;
       public            postgres    false    214            n           2606    33023    pedido pedido_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_pkey PRIMARY KEY (num_pedido);
 <   ALTER TABLE ONLY public.pedido DROP CONSTRAINT pedido_pkey;
       public            postgres    false    216            o           2606    33024    pedido pedido_ced_cliente_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.pedido
    ADD CONSTRAINT pedido_ced_cliente_fkey FOREIGN KEY (ced_cliente) REFERENCES public.cliente(cedula);
 H   ALTER TABLE ONLY public.pedido DROP CONSTRAINT pedido_ced_cliente_fkey;
       public          postgres    false    214    216    3180            �   Q   x�32��4772�L�+�ϫ�442615���s3s���s�� �9�R�K�9�LM�aLUF���E�� À
!$U1z\\\ A"w          V  x��ձN�@���}�Vg�].�����"1w	m�"�I�"ފg��p]Z�K)C�ɲ�_�ڬ�{��o��8���a�{��y)^��s	MI5����ۉ��>Gڍ�Ź��e<Z��ir��J'.��@i��=�T)δX���/�jLzU8z��Y;s�]?]��e
䉓�榄е���7��E�����
��!2o����{��4��ǻ�������v�:K���Xf�� ;��, G�,C��;uW%"�͕ݎ\<��z?���-Gl �Q�*(;@.c.b�5� �jGd�����/�d�N۾�A�T��Q
�ٮ���rq���c�q]ެ�sߌAl�     